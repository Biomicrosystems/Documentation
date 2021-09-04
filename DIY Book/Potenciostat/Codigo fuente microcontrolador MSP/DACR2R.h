/*
 * DACR2R.h
 *
 *  Created on: Mar 11, 2020
 *      Author: killan
 */

#ifndef DACR2R_H_
#define DACR2R_H_

#include <DACgenerator.h>

class DAC_R2R: public DAC_generator
{
public:
    DAC_R2R();
    int setValue(int16_t value);
};

#endif /* DACR2R_H_ */
