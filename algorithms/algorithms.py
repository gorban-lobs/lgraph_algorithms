from queue import Queue
from lgraph import LGraph


def stack_processing(trace_stack, cur_trace):
    traces = (
        {'trace_type': 'round', 'open': '(', 'closed': ')'},
        {'trace_type': 'square', 'open': '[', 'closed': ']'}
    )
    for trace in traces:
        trace_type = trace['trace_type']
        if cur_trace[trace_type]:
            if cur_trace[trace_type][0] == trace['open']:
                trace_stack[trace_type].append(cur_trace[trace_type])
            elif cur_trace[trace_type][0] == trace['closed']:
                if len(trace_stack[trace_type]) == 0 or \
                        trace_stack[trace_type][-1][1] != \
                        cur_trace[trace_type][1]:
                    return False
                else:
                    trace_stack[trace_type].pop()
    return True


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


def rest_direct(vert, direct_dict, trace):
    res_chains = []
    for edge in vert.edges:
        pass


def create_direct_dict(lgraph):
    direct_dict = dict()
    for init_vert in lgraph.initials:
        vert = init_vert.edges[0].end
        trace = {'round': [], 'square': []}
        full_chain = rest_direct(vert, direct_dict, trace)


if __name__ == '__main__':
    test_stack_processing()
