import os
from collections import Iterable
from stograde.common import run, flatten

from .truncate import truncate
from .cat import cat
from .pipe import pipe


def get_file(filename, results, options):
    file_status, file_contents = cat(filename)
    if file_status == 'success':
        _, last_edit, _ = run(['git', 'log', '-n', '1', '--pretty=format:%cd', '--', filename])
        results['last modified'] = last_edit

    if options['hide_contents']:
        file_contents = ''
    elif options['truncate_contents']:
        file_contents = truncate(file_contents, options['truncate_contents'])

    if file_status != 'success':
        results['missing'] = True
        results['other files'] = os.listdir('.')
        results['optional'] = options['optional']
        return False

    results['optional_compile'] = options['optional_compile']
    results['contents'] = file_contents
    return True


def compile_file(filename, *, steps, results, supporting_dir):
    for step in steps:
        command = step \
            .replace('$@', './' + filename) \
            .replace('$SUPPORT', supporting_dir)

        cmd, input_for_cmd = pipe(command)
        status, compilation, _ = run(cmd, timeout=30, input_data=input_for_cmd)

        results['compilation'].append({
            'command': command,
            'output': compilation,
            'status': status,
        })

        if status != 'success':
            return False

    return True


def test_file(filename, *, spec, tests, results, options, cwd, supporting_dir, interact):
    tests = flatten(tests + [test_spec['commands']
                             for test_spec in spec.get('tests', {})
                             if test_spec['filename'] == filename])

    for test_cmd in tests:
        if not test_cmd:
            continue

        test_cmd = test_cmd \
            .replace('$@', './' + filename) \
            .replace('$SUPPORT', supporting_dir)

        test_cmd, input_for_test = pipe(test_cmd)

        if os.path.exists(os.path.join(cwd, filename)):
            again = True
            while again:
                status, full_result, again = run(test_cmd,
                                                 input_data=input_for_test,
                                                 timeout=options['timeout'],
                                                 interact=interact)

                result = truncate(full_result, options['truncate_output'])
                was_truncated = (full_result != result)

                results['result'].append({
                    'command': test_cmd,
                    'status': status,
                    'output': result,
                    'truncated': was_truncated,
                    'truncated after': options['truncate_output'],
                })

        else:
            results['result'].append({
                'command': test_cmd,
                'error': True,
                'output': '{} could not be found.'.format(filename),
            })

    return True


def process_file(filename, *, steps, tests, options, spec, cwd, supporting_dir, interact, skip_web_compile):

    base_opts = {
        'timeout': 4,
        'truncate_output': 10000,  # 10K
        'truncate_contents': False,
        'optional': False,
        'optional_compile': False,
        'hide_contents': False,
        'web': False
    }
    base_opts.update(options)
    options = base_opts

    results = {
        'filename': filename,
        'missing': False,
        'compilation': [],
        'result': [],
    }

    should_continue = get_file(filename, results, options)
    if not should_continue or skip_web_compile and options['web']:
        return results

    should_continue = compile_file(filename,
                                   steps=steps,
                                   results=results,
                                   supporting_dir=supporting_dir)

    if not should_continue or not steps or options['web']:
        return results

    test_file(filename,
              spec=spec,
              tests=tests,
              results=results,
              options=options,
              cwd=cwd,
              supporting_dir=supporting_dir,
              interact=interact)

    return results
