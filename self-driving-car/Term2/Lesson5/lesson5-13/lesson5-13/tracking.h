//
//  tracking.hpp
//  lesson5-13
//
//  Created by Seonman Kim on 12/11/17.
//  Copyright © 2017 Seonman Kim. All rights reserved.
//

#ifndef FUSION_KF_H_
#define FUSION_KF_H_

#include "measurement_package.h"
#include <vector>
#include <string>
#include <fstream>
#include "kalman_filter.h"

class Tracking {
public:
    Tracking();
    virtual ~Tracking();
    void ProcessMeasurement(const MeasurementPackage &measurement_pack);
    KalmanFilter kf_;
    
private:
    bool is_initialized_;
    int64_t previous_timestamp_;
    
    //acceleration noise components
    float noise_ax;
    float noise_ay;
    
};

#endif /* FUSION_KF_H_ */

