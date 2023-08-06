8. Calibration of double ended measurement with WLS and confidence intervals
============================================================================

Calibration procedure
---------------------

A double ended calibration is performed with weighted least squares.
Over all timesteps simultaneous. :math:`\gamma` and :math:`\alpha`
remain constant, while :math:`C` varies over time. The weights are not
considered equal here. The weights kwadratically decrease with the
signal strength of the measured Stokes and anti-Stokes signals.

The confidence intervals can be calculated as the weights are correctly
defined.

The confidence intervals consist of two sources of uncertainty.

1. Measurement noise in the measured Stokes and anti-Stokes signals.
   Expressed in a single variance value.
2. Inherent to least squares procedures / overdetermined systems, the
   parameters are estimated with limited certainty and all parameters
   are correlated. Which is expressen in the covariance matrix.

Both sources of uncertainty are propagated to an uncertainty in the
estimated temperature via Monte Carlo.

.. code:: ipython3

    import os

    from dtscalibration import read_silixa_files
    import matplotlib.pyplot as plt
    %matplotlib inline


.. parsed-literal::

    /Users/bfdestombe/anaconda3/envs/dts/lib/python3.7/typing.py:845: FutureWarning: xarray subclass DataStore should explicitly define __slots__
      super().__init_subclass__(*args, **kwargs)


.. code:: ipython3

    filepath = os.path.join('..', '..', 'tests', 'data', 'double_ended2')

    ds_ = read_silixa_files(
        directory=filepath,
        timezone_netcdf='UTC',
        file_ext='*.xml')

    ds = ds_.sel(x=slice(0, 100))  # only calibrate parts of the fiber
    sections = {
        'probe1Temperature': [slice(7.5, 17.), slice(70., 80.)],  # cold bath
        'probe2Temperature': [slice(24., 34.), slice(85., 95.)],  # warm bath
        }
    ds.sections = sections


.. parsed-literal::

    6 files were found, each representing a single timestep
    6 recorded vars were found: LAF, ST, AST, REV-ST, REV-AST, TMP
    Recorded at 1693 points along the cable
    The measurement is double ended
    Reading the data from disk


.. code:: ipython3

    st_label = 'st'
    ast_label = 'ast'
    rst_label = 'rst'
    rast_label = 'rast'

First calculate the variance in the measured Stokes and anti-Stokes
signals, in the forward and backward direction.

The Stokes and anti-Stokes signals should follow a smooth decaying
exponential. This function fits a decaying exponential to each reference
section for each time step. The variance of the residuals between the
measured Stokes and anti-Stokes signals and the fitted signals is used
as an estimate of the variance in measured signals.

.. code:: ipython3

    st_var, resid = ds.variance_stokes(st_label=st_label)
    ast_var, _ = ds.variance_stokes(st_label=ast_label)
    rst_var, _ = ds.variance_stokes(st_label=rst_label)
    rast_var, _ = ds.variance_stokes(st_label=rast_label)

.. code:: ipython3

    resid.plot(figsize=(12, 8));



.. image:: 08Calibrate_double_wls.ipynb_files/08Calibrate_double_wls.ipynb_8_0.png


We calibrate the measurement with a single method call. The labels refer
to the keys in the DataStore object containing the Stokes, anti-Stokes,
reverse Stokes and reverse anti-Stokes. The variance in those
measurements were calculated in the previous step. We use a sparse
solver because it saves us memory.

.. code:: ipython3

    ds.calibration_double_ended(
        st_label=st_label,
        ast_label=ast_label,
        rst_label=rst_label,
        rast_label=rast_label,
        st_var=st_var,
        ast_var=ast_var,
        rst_var=rst_var,
        rast_var=rast_var,
        store_tmpw='tmpw',
        method='wls',
        solver='sparse')

.. code:: ipython3

    ds.tmpw.plot()




.. parsed-literal::

    <matplotlib.collections.QuadMesh at 0x12b63a5d0>




.. image:: 08Calibrate_double_wls.ipynb_files/08Calibrate_double_wls.ipynb_11_1.png


Confidence intervals
--------------------

With another method call we estimate the confidence intervals. If the
method is ``wls`` and confidence intervals are passed to ``conf_ints``,
confidence intervals calculated. As weigths are correctly passed to the
least squares procedure, the covariance matrix can be used as an
estimator for the uncertainty in the parameters. This matrix holds the
covariances between all the parameters. A large parameter set is
generated from this matrix as part of the Monte Carlo routine, assuming
the parameter space is normally distributed with their mean at the best
estimate of the least squares procedure.

The large parameter set is used to calculate a large set of
temperatures. By using ``percentiles`` or ``quantile`` the 95%
confidence interval of the calibrated temperature between 2.5% and 97.5%
are calculated.

The confidence intervals differ per time step. If you would like to
calculate confidence intervals of all time steps together you have the
option ``ci_avg_time_flag=True``. ‘We can say with 95% confidence that
the temperature remained between this line and this line during the
entire measurement period’. This is ideal if you’d like to calculate the
background temperature with a confidence interval.

.. code:: ipython3

    ds.conf_int_double_ended(
        p_val='p_val',
        p_cov='p_cov',
        st_label=st_label,
        ast_label=ast_label,
        rst_label=rst_label,
        rast_label=rast_label,
        st_var=st_var,
        ast_var=ast_var,
        rst_var=rst_var,
        rast_var=rast_var,
        store_tmpf='tmpf',
        store_tmpb='tmpb',
        store_tmpw='tmpw',
        store_tempvar='_var',
        conf_ints=[2.5, 50., 97.5],
        mc_sample_size=500,  # <- choose a much larger sample size
        ci_avg_time_flag=False)

.. code:: ipython3

    ds1 = ds.isel(time=-1)  # take only the first timestep
    ds1.tmpw.plot(linewidth=0.7, figsize=(12, 8))
    ds1.tmpw_mc.isel(CI=0).plot(linewidth=0.7, label='CI: 2.5%')
    ds1.tmpw_mc.isel(CI=2).plot(linewidth=0.7, label='CI: 97.5%')
    plt.legend();



.. image:: 08Calibrate_double_wls.ipynb_files/08Calibrate_double_wls.ipynb_15_0.png


The DataArrays ``tmpf_mc`` and ``tmpb_mc`` and the dimension ``CI`` are
added. ``MC`` stands for monte carlo and the ``CI`` dimension holds the
confidence interval ‘coordinates’.

.. code:: ipython3

    (ds1.tmpw_mc_var**0.5).plot(figsize=(12, 4));
    plt.ylabel('$\sigma$ ($^\circ$C)');



.. image:: 08Calibrate_double_wls.ipynb_files/08Calibrate_double_wls.ipynb_17_0.png


.. code:: ipython3

    ds.data_vars




.. parsed-literal::

    Data variables:
        ST                     (x, time) float64 4.049e+03 4.044e+03 ... 3.501e+03
        AST                    (x, time) float64 3.293e+03 3.296e+03 ... 2.803e+03
        REV-ST                 (x, time) float64 4.061e+03 4.037e+03 ... 4.584e+03
        REV-AST                (x, time) float64 3.35e+03 3.333e+03 ... 3.707e+03
        TMP                    (x, time) float64 16.69 16.87 16.51 ... 13.6 13.69
        acquisitionTime        (time) float32 2.098 2.075 2.076 2.133 2.085 2.062
        referenceTemperature   (time) float32 21.0536 21.054 ... 21.0531 21.057
        probe1Temperature      (time) float32 4.36149 4.36025 ... 4.36021 4.36118
        probe2Temperature      (time) float32 18.5792 18.5785 ... 18.5805 18.5723
        referenceProbeVoltage  (time) float32 0.121704 0.121704 ... 0.121705
        probe1Voltage          (time) float32 0.114 0.114 0.114 0.114 0.114 0.114
        probe2Voltage          (time) float32 0.121 0.121 0.121 0.121 0.121 0.121
        userAcquisitionTimeFW  (time) float32 2.0 2.0 2.0 2.0 2.0 2.0
        userAcquisitionTimeBW  (time) float32 2.0 2.0 2.0 2.0 2.0 2.0
        gamma                  float64 482.6
        alpha                  (x) float64 -0.007229 -0.003373 ... -0.005238
        df                     (time) float64 1.465 1.466 1.465 1.465 1.465 1.465
        db                     (time) float64 1.465 1.465 1.464 1.465 1.466 1.464
        gamma_var              float64 0.03742
        alpha_var              (x) float64 2.611e-07 2.691e-07 ... 2.712e-07
        df_var                 (time) float64 5.256e-07 5.256e-07 ... 5.256e-07
        db_var                 (time) float64 5.267e-07 5.267e-07 ... 5.268e-07
        tmpf                   (x, time) float64 16.79 17.01 16.29 ... 13.57 13.74
        tmpb                   (x, time) float64 16.81 16.86 16.91 ... 13.67 13.71
        tmpf_mc_var            (x, time) float64 dask.array<chunksize=(787, 6), meta=np.ndarray>
        tmpb_mc_var            (x, time) float64 dask.array<chunksize=(787, 6), meta=np.ndarray>
        tmpw                   (x, time) float64 dask.array<chunksize=(787, 6), meta=np.ndarray>
        tmpw_mc_var            (x, time) float64 dask.array<chunksize=(787, 6), meta=np.ndarray>
        p_val                  (params1) float64 482.6 1.465 ... -0.005343 -0.005238
        p_cov                  (params1, params2) float64 0.03742 ... 2.712e-07
        tmpf_mc                (CI, x, time) float64 dask.array<chunksize=(3, 787, 6), meta=np.ndarray>
        tmpb_mc                (CI, x, time) float64 dask.array<chunksize=(3, 787, 6), meta=np.ndarray>
        tmpw_mc                (CI, x, time) float64 dask.array<chunksize=(3, 787, 6), meta=np.ndarray>



