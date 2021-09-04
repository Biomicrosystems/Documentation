/*
 * SWASV.h
 *
 *  Created on: 18 mar. 2020
 *      Author: killan
 */

#ifndef SWASV_H_
#define SWASV_H_

#include <msp430.h>
#include <boardMSP.h>
#include <Technique.h>
#include <DACR2R.h>

namespace msp
{

class SWASV: public Technique
{
public:
    SWASV();
    uint16_t getCurrentValue();
    uint16_t NextValue();
    uint8_t StopCondition();
    void processData(char *data, int len);
private:
    /* Variables */
    uint16_t StartValue;
    uint16_t TimeHold;
    uint16_t FinalValue;

    uint16_t CurrentValue;

    uint8_t ScanRate;

    bool Direction = false;
};

} /* namespace msp */

#endif /* SWASV_H_ */
