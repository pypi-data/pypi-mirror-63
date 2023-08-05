import oommfc as oc
from .driver import Driver


class MinDriver(Driver):
    """Energy minimisation driver.

    Only parameters which are defined in ``_allowed_attributes`` can be passed.

    Examples
    --------
    1. Defining driver with no keyword arguments.

    >>> import oommfc as oc
    ...
    >>> md = oc.MinDriver()

    2. Passing an argument which is not allowed

    >>> import oommfc as oc
    ...
    >>> md = oc.MinDriver(myarg=3)
    Traceback (most recent call last):
       ...
    AttributeError: ...

    """
    _allowed_attributes = ['evolver',
                           'stopping_mxHxm',
                           'stage_iteration_limit',
                           'total_iteration_limit',
                           'stage_count',
                           'stage_count_check',
                           'checkpoint_file',
                           'checkpoint_interval',
                           'checkpoint_disposal',
                           'start_iteration',
                           'start_stage',
                           'start_stage_iteration',
                           'start_stage_start_time',
                           'start_stage_elapsed_time',
                           'start_last_timestep',
                           'normalize_aveM_output',
                           'report_max_spin_angle',
                           'report_wall_time']

    def _script(self, system):
        # Save initial magnetisation.
        m0mif, m0name, Msname = oc.script.setup_m0(system.m, 'm0')
        mif = m0mif

        # Evolver
        if not hasattr(self, 'evolver'):
            self.evolver = oc.CGEvolver()
        if isinstance(self.evolver, oc.CGEvolver):
            mif += self.evolver._script
        else:
            msg = f'Cannot use {type(self.evolver)} for evolver.'
            raise TypeError(msg)

        # Minimisation driver
        mif += '# MinDriver\n'
        mif += 'Specify Oxs_MinDriver {\n'
        mif += '  evolver :evolver\n'
        mif += '  mesh :mesh\n'
        mif += f'  Ms :{Msname}\n'
        mif += f'  m0 :{m0name}\n'

        # Setting stopping mxHxm default value.
        if not hasattr(self, 'stopping_mxHxm'):
            self.stopping_mxHxm = 0.01

        # Other parameters for MinDriver
        for attr in self._allowed_attributes:
            if hasattr(self, attr) and attr != 'evolver':
                mif += f'  {attr} {getattr(self, attr)}\n'

        mif += '}\n\n'

        # Saving results
        mif += 'Destination table mmArchive\n'
        mif += 'Destination mags mmArchive\n\n'
        mif += 'Schedule DataTable table Stage 1\n'
        mif += 'Schedule Oxs_MinDriver::Magnetization mags Stage 1'

        return mif

    def _checkargs(self, **kwargs):
        pass
