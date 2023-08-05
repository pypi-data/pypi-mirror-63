import numpy as np
import os.path
import subprocess
import tempfile
import warnings
import os
from subprocess import PIPE
import time
from shutil import copyfile


def odegetdp(fun, trange, varargin, dir, fargin=None, mesh=None):
    if fargin is None:
        fargin = []

    getdpopts = varargin.copy()
    funarguments = fargin

    if not isnumeric(trange) or not isinstance(trange, np.ndarray):
        raise Exception('Octave:invalid-input-arg', 'odegetp: TRANGE must be a numeric vector')

    if np.size(trange) < 2:
        raise Exception('Octave:invalid-input-arg', 'odegetp: TRANGE must contain at least 2 elements')
    if trange[0] >= trange[1]:
        raise Exception('Octave:invalid-input-arg', 'odegetp: invalid time span, TRANGE(1) >= TRANGE(2)')

    # Check if model exists
    if not isinstance(fun, str):
        fun = fun.__name__

    fdir, file = os.path.split(fun)
    fname, fext = os.path.splitext(file)
    if not os.path.isfile(fun) or not fext == '.pro':
        raise Exception('Octave:invalid-input-arg', 'odegetdp: FUN must be a valid getdp FUN.pro file')
    else:  # get absolute path
        fdir = fdir

    # Check for getdp executable
    if 'Executable' not in getdpopts:
        getdpopts['Executable'] = 'getdp'

    version_test = subprocess.run([getdpopts['Executable'], '--version'], stdout=PIPE, stderr=PIPE)
    if version_test.returncode:
        raise Exception('Octave:invalid-input-arg',
                        'odegetdp: getdp not found, you may use "Executable" in the option structure.')
    else:
        getdpver = version_test.stderr.decode("utf-8")[0:5]

    if 'Verbose' not in getdpopts:
        getdpopts['Verbose'] = 0

    # Choose TimeStep
    if 'TimeStep' not in getdpopts:
        getdpopts['TimeStep'] = (trange[-1] - trange[0]) / 50
        print('odegetdp: choosing default time step dt=' + str(getdpopts['TimeStep']) + 's')
    elif getdpopts['TimeStep'] <= 0:
        raise Exception('Octave:invalid-input-arg', 'odegetdp: Time step must be positive.')

    # Process optional funarguments
    funargstr = ''
    for i in range(0, len(funarguments), 2):
        if isnumeric(funarguments[i + 1]):
            funargstr = funargstr + ' -setnumber ' + funarguments[i] + ' ' + str(funarguments[i + 1])
        else:
            funargstr = funargstr + ' -setstring ' + funarguments[i] + ' ' + funarguments[i + 1]
    funargstr = funargstr[1:]
    # Choose PreProcessing
    if 'PreProcessing' not in getdpopts:
        getdpopts['PreProcessing'] = '#1'
        # print('odegetdp: choosing default PreProcessing "#1"')

    # Choose first Resolution
    if 'Resolution' not in getdpopts:
        getdpopts['Resolution'] = '#1'
        # print('odegetdp: choosing default Resolution "#1"')

    # Check if mesh exists
    if mesh is not None:
        mshfile = os.path.join(fdir, mesh)
    else:
        mshfile = os.path.join(fdir, fname + '.msh')
    if not os.path.exists(mshfile):
        raise Exception('odegetdp: run gmsh on beforehand to create a msh-file: ' + mshfile)

    # Create a file with the given initial value
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpname = os.path.join(tmpdir, fname)
        resdir = os.path.join(tmpdir, 'res')
        prefile = os.path.join(tmpdir, fname + '.pre')
        resfile = os.path.join(tmpdir, fname + '.res')
        joule_file = os.path.join(tmpdir, 'resJL.dat')
        ua_file = os.path.join(tmpdir, 'resUa.dat')
        ub_file = os.path.join(tmpdir, 'resUb.dat')
        uc_file = os.path.join(tmpdir, 'resUc.dat')
        ia_file = os.path.join(tmpdir, 'resIa.dat')
        ib_file = os.path.join(tmpdir, 'resIb.dat')
        ic_file = os.path.join(tmpdir, 'resIc.dat')

        # start = time.time()
        # Do preprocessing step
        exe_string = [getdpopts['Executable'],
                      fun,
                      '-pre "' + getdpopts['PreProcessing'] + '"',
                      '-msh', mshfile,
                      '-name', tmpname,
                      '-res', resfile,
                      '-setnumber timemax', str(trange[1]),
                      '-setnumber dtime', str(getdpopts['TimeStep']),
                      '-setstring ResDir', resdir,
                      funargstr]

        if getdpopts['Verbose'] == 1:
            status = subprocess.run(' '.join(exe_string), shell=True)
        else:
            status = subprocess.run(' '.join(exe_string), shell=True, stdout=PIPE, stderr=PIPE)

        if status.returncode:
            raise Exception('odegetdp: preprocessing failed')

        copyfile(prefile, os.path.join(dir, str(trange[1])))

    return


def set_resolution_old(file, t, x, numdofs):
    with open(file, "w") as fid:
        # get positions of dofdata in x vector
        dofpos = np.cumsum([0, numdofs])
        # start writing res file
        fid.write('$ResFormat /* GetDP 2.10.0, ascii */\n')
        fid.write('1.1 0\n')
        fid.write('$EndResFormat\n')
        for j in range(np.size(t)):
            for k in range(np.size(numdofs)):
                fid.write('$Solution  /* DofData #' + str(k) + ' */\n')
                fid.write(str(k) + ' ' + str(t) + ' 0 ' + str(j) + '\n')
                y = x[dofpos[k]: dofpos[k + 1]]
                fid.write("\n".join(" ".join(map(str, line)) for line in np.vstack((np.real(y), np.imag(x))).T))
                fid.write('\n$EndSolution\n')
    if np.max(np.isnan(x)) or np.max(np.isnan(t)):
        warnings.warn('odegetdp: something went wrong')


def set_resolution(file, t, x, numdofs):
    dofpos = np.cumsum([0, numdofs])
    com_str = ['$ResFormat /* GetDP 2.10.0, ascii */', '1.1 0', '$EndResFormat']

    for j in range(np.size(t)):
        for k in range(np.size(numdofs)):
            com_str.append('$Solution  /* DofData #' + str(k) + ' */')
            com_str.append(str(k) + ' ' + str(t) + ' 0 ' + str(j))
            y = x[dofpos[k]: dofpos[k + 1]]
            com_str.append("\n".join(" ".join(map(str, line)) for line in np.vstack((np.real(y), np.imag(x))).T))
            com_str.append('$EndSolution\n')

    with open(file, "w") as fid:
        fid.write("\n".join(com_str))
    if np.max(np.isnan(x)) or np.max(np.isnan(t)):
        warnings.warn('odegetdp: something went wrong')


def get_preresolution(file):
    with open(file) as f:
        content = f.readlines()
    ind = [idx for idx, s in enumerate(content) if '$DofData' in s][0]
    tmp = content[ind + 5].split()[-1]

    return int(tmp)


def get_values_from(file):
    joule = []
    with open(file) as fobj:
        for line in fobj:
            row = line.split()
            joule.append(row[-1])
    return np.array(joule, dtype=float)


def getdp_read_resolution(file, numdofs):
    # init solution vector, may contain several dofdata sets
    x = np.zeros((0, np.sum(numdofs)))
    # init vector of time steps
    t = np.zeros(0)
    # init vector of time step numbers
    j = 0
    oldstep = 0
    # get positions of dofdata in x vector
    dofpos = np.cumsum([0, numdofs])

    with open(file) as f:
        content = f.readlines()

    idx = 0
    while idx < len(content):
        if content[idx].find('$Solution') != -1:
            idx = idx + 1
            line = content[idx]
            idx = idx + 1
            tmp = line.split()
            tmp = [int(tmp[0]), float(tmp[1]), float(tmp[2]), int(tmp[3])]
            if oldstep < 1 + tmp[3]:
                j = j + 1
                oldstep = 1 + tmp[3]
                x = np.vstack((x, np.zeros((1, np.sum(numdofs)))))
                t = np.hstack((t, 0))
            elif oldstep > 1 + tmp[3]:
                raise Exception('odegetdp: raise Exception reading file #s. time step #d is stored after #d', file,
                                tmp[3], oldstep - 1)
            k = 1 + tmp[0]
            t[j - 1] = tmp[1]
            # read complex dofdata set into solution vector
            xtmp = content[idx:idx + numdofs]
            xtmp = np.array([list(map(float, s.split())) for s in xtmp])
            x[j - 1, dofpos[k - 1]:dofpos[k] + 1] = (xtmp[:, 0] + np.imag(xtmp[:, 1])).T
            idx = idx + numdofs

        elif content[idx].find('$ResFormat') != -1:
            idx = idx + 1
            if not content[idx][0:3] == '1.1':
                raise Exception('odegetdp: unknown file format version')
        else:
            idx = idx + 1

    if np.max(np.isnan(x)) or np.max(np.isnan(t)):
        raise Exception('getdp_read_resolution: file contains NaN')

    return t, x


def isnumeric(obj):
    try:
        obj + 0
        return True
    except TypeError:
        return False
