from 


def test_stack_processing():
    trace_stack = {'round': [('(', 1)], 'square': []}
    cur_trace = {'round': (')', 1), 'square': ''}
    assert stack_processing(trace_stack, cur_trace) == True
    print('1:', trace_stack)

    trace_stack = {'round': [('(', 1)], 'square': []}
    cur_trace = {'round': (')', 2), 'square': ''}
    assert stack_processing(trace_stack, cur_trace) == False
    print('2:', trace_stack)

    trace_stack = {'round': [('(', 1)], 'square': []}
    cur_trace = {'round': (')', 2), 'square': ''}
    assert stack_processing(trace_stack, cur_trace) == False
    print('3:', trace_stack)

    trace_stack = {'round': [('(', 1)], 'square': [('[', 1), ('[', 2)]}
    cur_trace = {'round': (')', 1), 'square': (']', 2)}
    assert stack_processing(trace_stack, cur_trace) == True
    print('4:', trace_stack)

    trace_stack = {'round': [('(', 1)], 'square': []}
    cur_trace = {'round': ('(', 2), 'square': ('[', 3)}
    assert stack_processing(trace_stack, cur_trace) == True
    print('5:', trace_stack)