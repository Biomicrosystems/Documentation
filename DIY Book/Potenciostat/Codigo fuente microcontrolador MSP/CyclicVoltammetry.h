/*
 * CyclicVoltammetry.h
 *
 *  Created on: Mar 11, 2020
 *      Author: killan
 */

#ifndef CYCLICVOLTAMMETRY_H_
#define CYCLICVOLTAMMETRY_H_

#include <msp430.h>
#include <boardMSP.h>
#include <Technique.h>
#include <DACR2R.h>

class CyclicVoltammetry: public Technique
{
public:
    /* Variables */

public:
    /* Methods */
    CyclicVoltammetry();
    uint16_t NextValue();
    uint16_t getCurrentValue();
    void processData(char *data, int len);
    uint8_t StopCondition();

private:
    /* Private variables */
    bool Direction;
    uint16_t PreviousValue;
    uint16_t StartPoint;
    uint16_t FirstVertex;
    uint16_t SecondVertex;
    uint8_t ZeroCrossNum;

    int16_t CurrentValue;
    int8_t CurrentZerosCrossed;
    uint16_t Speed;
};

#endif /* CYCLICVOLTAMMETRY_H_ */
