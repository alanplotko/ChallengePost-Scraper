from ml import predictOneVsAll
import sys
import numpy as np
from scraper import parseProject

def main():
    #load stuff
    npzfile = np.load('learned_data.npz')
    all_theta = npzfile['all_theta']
    mu = npzfile['mu']
    sigma = npzfile['sigma']
    ex = parseProject(sys.argv[1])

    norms = np.array([])
    for i in range(ex.shape[0]):
    	norms = np.append(norms, (ex[i] - mu[i]) / sigma[i])

    norms = np.reshape(norms, (1, -1))

    print(ex)
    p = predictOneVsAll(all_theta, norms)
    print(p)


if __name__ == "__main__":
    main()
