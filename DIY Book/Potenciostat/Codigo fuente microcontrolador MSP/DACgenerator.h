/*
 * DACgenerator.h
 *
 *  Created on: Mar 11, 2020
 *      Author: killan
 */

#ifndef DACGENERATOR_H_
#define DACGENERATOR_H_

#include <msp430.h>
#include <stdint.h>
#include <stddef.h>

class DAC_generator
{
public:
    DAC_generator();
    virtual int setValue(int16_t value)=0;
};

#endif /* DACGENERATOR_H_ */
