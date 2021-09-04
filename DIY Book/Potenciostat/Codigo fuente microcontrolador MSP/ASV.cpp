/*
 * ASV.cpp
 *
 *  Created on: Mar 11, 2020
 *      Author: killan
 */

#include <ASV.h>

ASV::ASV()
{
    // Initialize data
    dac = new DAC_R2R();
    this->Direction = false;
    this->StartValue = 1000;
    this->TimeHold = 500;
    this->FinalValue = 2500;
    this->ScanRate = 10;
}

uint16_t ASV::NextValue()
{
    active = true;
    if (this->TimeHold == 0)
    {
        if (this->Direction)
            this->CurrentValue += this->ScanRate;
        else
            this->CurrentValue -= this->ScanRate;
    }
    else
    {
        this->TimeHold--;
    }

    if (this->Direction)
    {
        if (this->CurrentValue >= this->FinalValue)
        {
            active = false;
            this->CurrentValue = this->FinalValue;
        }
    }
    else
    {
        if (this->CurrentValue <= this->FinalValue)
        {
            active = false;
            this->CurrentValue = this->FinalValue;
        }
    }
    return active;
}

uint16_t ASV::getCurrentValue()
{
    return this->CurrentValue;
}

void ASV::processData(char *data, int len)
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

uint8_t ASV::StopCondition()
{
    if (this->CurrentValue == this->FinalValue)
        return true;
    else
        return false;
}
