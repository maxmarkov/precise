import random
from precise.skatervaluation.managercomparisonutil.managertesting import manager_test_run, manager_debug_run
from precise.skaters.managers.rpmanagers import rp_ewa_r01_p40_l21_long_manager as troublesome_mgr


def test_random_manager():
    from precise.skaters.managers.rpmanagers import RP_STOCHASTIC_LONG_MANAGERS
    HULL = [s for s in RP_STOCHASTIC_LONG_MANAGERS if 'l21' in s.__name__]
    mgr = random.choice(HULL)
    j = random.choice([1, 5, 20])
    q = random.choice([1.0, 0.1])
    manager_test_run(mgr=mgr, j=j, q=q)


if __name__ == '__main__':
    manager_debug_run(troublesome_mgr, n_dim=500, n_obs=2000)
    if False:
        for _ in range(20):
            test_random_manager()
