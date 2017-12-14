//
//  kalman_filter.hpp
//  lesson5-13
//
//  Created by Seonman Kim on 12/11/17.
//  Copyright © 2017 Seonman Kim. All rights reserved.
//

#ifndef KALMAN_FILTER_H_
#define KALMAN_FILTER_H_
#include "Dense"

using Eigen::MatrixXd;
using Eigen::VectorXd;

class KalmanFilter {
public:
    
    ///* state vector
    VectorXd x_;
    
    ///* state covariance matrix
    MatrixXd P_;
    
    ///* state transistion matrix
    MatrixXd F_;
    
    ///* process covariance matrix
    MatrixXd Q_;
    
    ///* measurement matrix
    MatrixXd H_;
    
    ///* measurement covariance matrix
    MatrixXd R_;
    
    /**
     * Constructor
     */
    KalmanFilter();
    
    /**
     * Destructor
     */
    virtual ~KalmanFilter();
    
    /**
     * Predict Predicts the state and the state covariance
     * using the process model
     */
    void Predict();
    
    /**
     * Updates the state and
     * @param z The measurement at k+1
     */
    void Update(const VectorXd &z);
    
};

#endif /* KALMAN_FILTER_H_ */


