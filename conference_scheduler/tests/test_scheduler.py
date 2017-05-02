import numpy as np
from collections import Counter
from conference_scheduler import scheduler


def test_constraint_violations(valid_solution, shape, sessions, events):
    violations = scheduler.constraint_violations(
        valid_solution, shape, sessions, events)
    assert len(violations) == 0

    # solution with event 1 not scheduled
    solution = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = scheduler.constraint_violations(
        solution, shape, sessions, events)
    assert violations == ['schedule_all_events event: 1']

    # solution with event 0 scheduled twice
    solution = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    violations = scheduler.constraint_violations(
        solution, shape, sessions, events)
    assert violations == ['max_one_event_per_slot slot: 0']

    # solution where two talks are in same session but share no tag
    solution = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0]
    ])
    violations = scheduler.constraint_violations(
        solution, shape, sessions, events)
    assert violations == [
        'events_in_session_share_a_tag: 0 slot: 0',
        'events_in_session_share_a_tag: 2 slot: 1'
    ]


def test_is_valid_solution(valid_solution, shape, sessions, events):
    assert scheduler.is_valid_solution(valid_solution, shape, sessions, events)

    # Test that an empty solution is invalid
    solution = []
    assert not scheduler.is_valid_solution(solution, shape, sessions, events)

    # solution with event 1 scheduled twice
    solution = np.array([
        [1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0]
    ])
    assert not scheduler.is_valid_solution(solution, shape, sessions, events)


def test_schedule_has_content(solution):
    assert len(solution) > 0


def test_all_events_scheduled(shape, solution):
    scheduled_events = [item[0] for item in solution]
    for event in range(shape.events):
        assert event in scheduled_events


def test_slots_scheduled_once_only(solution):
    for slot, count in Counter(item[1] for item in solution).items():
        assert count <= 1


def test_events_scheduled_once_only(solution):
    for event, count in Counter(item[0] for item in solution).items():
        assert count == 1
