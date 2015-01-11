from ml import trainOneVsAll
import numpy as np

def main():
    #load stuff
    npzfile = np.load('training_data.npz')
    X = npzfile['X']
    y = npzfile['y']
    input_layer_size = X.shape[0]
    num_labels = 2

    #print(X)
    #print(y)

    lam = 3
    all_theta, mu, sigma = trainOneVsAll(X, y, num_labels, lam)
    print(all_theta)
    np.savez("learned_data.npz", all_theta=all_theta, mu=mu, sigma=sigma)


if __name__ == "__main__":
    main()
