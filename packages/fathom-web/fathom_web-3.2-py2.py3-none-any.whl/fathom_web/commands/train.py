from json import load
from pprint import pformat

from click import argument, command, File, option, progressbar
from tensorboardX import SummaryWriter
from torch import tensor
from torch.nn import BCEWithLogitsLoss
from torch.optim import Adam

from ..accuracy import accuracy_per_tag, accuracy_per_page, pretty_accuracy
from ..utils import classifier, mini_histogram, tensors_from


def learn(learning_rate, iterations, x, y, validation=None, stop_early=False, run_comment='', pos_weight=None, layers=[]):
    # Define a neural network using high-level modules.
    writer = SummaryWriter(comment=run_comment)
    model = classifier(len(x[0]), len(y[0]), layers)
    if pos_weight:
        pos_weight = tensor([pos_weight])
    loss_fn = BCEWithLogitsLoss(reduction='sum', pos_weight=pos_weight)  # reduction=mean converges slower.
    # TODO: Maybe also graph using add_pr_curve(), which can show how that tradeoff is going.
    optimizer = Adam(model.parameters(), lr=learning_rate)

    if validation:
        validation_ins, validation_outs = validation
        previous_validation_loss = None
    stopped_early = False
    with progressbar(range(iterations)) as bar:
        for t in bar:
            y_pred = model(x)  # Make predictions.
            loss = loss_fn(y_pred, y)
            writer.add_scalar('loss', loss, t)
            if validation:
                validation_loss = loss_fn(model(validation_ins), validation_outs)
                if stop_early:
                    if previous_validation_loss is not None and previous_validation_loss < validation_loss:
                        stopped_early = True
                        model.load_state_dict(previous_model)  # noqa: previous_model will always be defined here, but the linter can't follow the logic.
                        break
                    else:
                        previous_validation_loss = validation_loss
                        previous_model = model.state_dict()
                writer.add_scalar('validation_loss', validation_loss, t)
            accuracy, _, _ = accuracy_per_tag(y, y_pred)
            writer.add_scalar('training_accuracy_per_tag', accuracy, t)
            optimizer.zero_grad()  # Zero the gradients.
            loss.backward()  # Compute gradients.
            optimizer.step()
    if stopped_early:
        print(f'Stopping early at iteration {t}, just before validation error rose.')

    # Horizontal axis is what confidence. Vertical is how many samples were that confidence.
    writer.add_histogram('confidence', confidences(model, x), t)
    writer.close()
    return model


def confidences(model, x):
    return model(x).sigmoid()


def pretty_coeffs(model, feature_names):
    """Format coefficient and bias numbers for easy pasting into JS."""
    dict_params = {}
    for name, param in model.named_parameters():
        dict_params[name] = param.data.tolist()
    if '2.weight' in dict_params:  # There are hidden layers.
        return pformat(dict_params, compact=True)
    else:
        pretty = ',\n        '.join(f'["{k}", {v}]' for k, v in zip(feature_names, dict_params['0.weight'][0]))
        return ("""{{"coeffs": [
            {coeffs}
        ],
     "bias": {bias}}}""".format(coeffs=pretty, bias=dict_params['0.bias'][0]))


@command()
@argument('training_file',
          type=File('r'))
@option('validation_file', '-a',
        type=File('r'),
        help="A file of validation samples from FathomFox's Vectorizer, used to graph validation loss so you can see when you start to overfit")
@option('--stop-early', '-s',
        default=False,
        is_flag=True,
        help='Stop 1 iteration before validation loss begins to rise, to avoid overfitting. Before using this, make sure validation loss is monotonically decreasing.')
@option('--learning-rate', '-l',
        default=1.0,
        show_default=True,
        help='The learning rate to start from')
@option('--iterations', '-i',
        default=1000,
        show_default=True,
        help='The number of training iterations to run through')
@option('--pos-weight', '-p',
        type=float,
        default=None,
        show_default=True,
        help='The weighting factor given to all positive samples by the loss function. See: https://pytorch.org/docs/stable/nn.html#bcewithlogitsloss')
@option('--comment', '-c',
        default='',
        help='Additional comment to append to the Tensorboard run name, for display in the web UI')
@option('--quiet', '-q',
        default=False,
        is_flag=True,
        help='Hide per-page diagnostics that may help with ruleset debugging.')
@option('layers', '--layer', '-y',
        type=int,
        multiple=True,
        help='Add a hidden layer of the given size. You can specify more than one, and they will be connected in the given order. EXPERIMENTAL.')
def main(training_file, validation_file, stop_early, learning_rate, iterations, pos_weight, comment, quiet, layers):
    """Compute optimal coefficients for a Fathom ruleset, based on a set of
    labeled pages exported by the FathomFox Vectorizer.

    To see graphs of the results, install TensorBoard, then run this:
    tensorboard --logdir runs/.

    Some vocab used in the output messages:

      target -- A "right answer" DOM node, one that should be recognized

      candidate -- Any node (target or not) brought into the ruleset, by a
      dom() call, for consideration

      negative sample -- A sample with no intended target nodes, used to bait
      the recognizer into a false-positive choice

    """
    layers = list(layers)  # Comes in as tuple
    full_comment = '.LR={l},i={i}{c}'.format(
        l=learning_rate,
        i=iterations,
        c=(',' + comment) if comment else '')
    training_data = load(training_file)
    x, y, num_yes = tensors_from(training_data['pages'], shuffle=True)
    if validation_file:
        validation_data = load(validation_file)
        validation_ins, validation_outs, validation_yes = tensors_from(validation_data['pages'])
        validation_arg = validation_ins, validation_outs
    else:
        validation_arg = None
    model = learn(learning_rate,
                  iterations,
                  x,
                  y,
                  validation=validation_arg,
                  stop_early=stop_early,
                  run_comment=full_comment,
                  pos_weight=pos_weight,
                  layers=layers)
    print(pretty_coeffs(model, training_data['header']['featureNames']))
    accuracy, false_positives, false_negatives = accuracy_per_tag(y, model(x))
    print(pretty_accuracy(('  ' if validation_file else '') + 'Training accuracy per tag: ',
                          accuracy,
                          len(x),
                          false_positives,
                          false_negatives,
                          num_yes))
    if validation_file:
        accuracy, false_positives, false_negatives = accuracy_per_tag(validation_outs, model(validation_ins))
        print(pretty_accuracy('Validation accuracy per tag: ',
                              accuracy,
                              len(validation_ins),
                              false_positives,
                              false_negatives,
                              validation_yes))
    accuracy, training_report = accuracy_per_page(model, training_data['pages'])
    print(pretty_accuracy(('  ' if validation_file else '') + 'Training accuracy per page:',
                          accuracy,
                          len(training_data['pages'])))
    if validation_file:
        accuracy, validation_report = accuracy_per_page(model, validation_data['pages'])
        print(pretty_accuracy('Validation accuracy per page:',
                              accuracy,
                              len(validation_data['pages'])))

    if training_data['pages'] and 'time' in training_data['pages'][0]:
        times = [p['time'] for p in training_data['pages']]
        if validation_file and validation_data['pages'] and 'time' in validation_data['pages'][0]:
            times.extend([p['time'] for p in validation_data['pages']])
        print('\nTime per page (ms):',
              mini_histogram(times))

    if not quiet:
        print('\nTraining per-page results:\n', training_report, sep='')
        if validation_file:
            print('\nValidation per-page results:\n', validation_report, sep='')
    # TODO: Print "8000 elements. 7900 successes. 50 false positive. 50 false negatives."
