/*
 * SWASV.cpp
 *
 *  Created on: 18 mar. 2020
 *      Author: killan
 */

#include <SWASV.h>

namespace msp
{

SWASV::SWASV()
{
    // TODO Auto-generated constructor stub
    dac = new DAC_R2R();

}

uint16_t SWASV::getCurrentValue()
{
    return this->CurrentValue;
}

uint16_t SWASV::NextValue()
{
    return active;
}

uint8_t SWASV::StopCondition()
{
    return 0;
}

void SWASV::processData(char *data, int len)
{
    active = false;
    switch (data[0])
    {
    case StartMeasurement: /* 0x01 */
        Direction = (this->CurrentValue < this->FinalValue);
        active = true;
        break;
    case StoptMeasurement: /* 0x02 */
        active = false;
        break;
    case SetStartPoint: /* 0x03 */
        this->StartValue = data[2];
        this->StartValue = ((this->StartValue << 6) & 0xFC0) | data[1];
        this->CurrentValue = this->StartValue;
        break;
    case SetTimeHold: /* 0x11 */
        this->TimeHold = data[2];
        this->TimeHold = ((this->TimeHold << 6) & 0xFC0) | data[1];
        this->TimeHold += 1;
        break;
    case SetFinalValue: /* 0x12 */
        this->FinalValue = data[2];
        this->FinalValue = ((this->FinalValue << 6) & 0xFC0) | data[1];
        break;
    case setSpeedVal: /* 0x07 */
        this->ScanRate = data[2];
        this->ScanRate = ((this->ScanRate << 6) & 0xFC0) | data[1];
        break;
    default:
        break;
    }
}

} /* namespace msp */
