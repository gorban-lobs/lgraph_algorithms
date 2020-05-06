from lgraph import LGraph
from algorithms import stack_processing, create_direct_dict


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


def test_create_direct_dict():
    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '2', label='a')
    lg.add_edge('2', lg.final_main.name)
    print('0:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '2', label='a')
    lg.add_edge('1', '3', label='a')
    print('1:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '2', label='a')
    lg.add_edge('1', '3', label='a')
    lg.add_edge('2', lg.final_main.name)
    lg.add_edge('3', 'finals_1')
    print('2:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', lg.final_main.name)
    lg.add_edge('1', '2', label='a')
    lg.add_edge('2', 'finals_1')
    print('3:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '2', label='a')
    lg.add_edge('2', '2', label='a')
    lg.add_edge('2', '3', label='c')
    print('4:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '2')
    lg.add_edge('2', '2', label='a')
    lg.add_edge('2', '3', label='c')
    lg.add_edge('2', '4', label='b')
    lg.add_edge('4', 'finals_1')
    print('5:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '2')
    lg.add_edge('2', '2', label='a')
    lg.add_edge('2', '3', label='c')
    lg.add_edge('2', '4', label='a')
    lg.add_edge('4', 'finals_1')
    print('6:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '2', label='a', round_trace=('(', 1))
    lg.add_edge('2', '2', label='a')
    lg.add_edge('2', '3', label='c', round_trace=(')', 1))
    lg.add_edge('2', '4', label='a', round_trace=(')', 2))
    lg.add_edge('4', 'finals_1')
    print('7:', create_direct_dict(lg))

if __name__ == '__main__':
    test_create_direct_dict()
