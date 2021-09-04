/*
 * CyclicVoltammetry.cpp
 *
 *  Created on: Mar 11, 2020
 *      Author: killan
 */

#include <CyclicVoltammetry.h>

CyclicVoltammetry::CyclicVoltammetry()
{
    dac = new DAC_R2R();

    this->ZeroCrossNum = 4;
    this->StartPoint = 2047;
    this->FirstVertex = 2500;
    this->SecondVertex = 1500;
    this->CurrentValue = this->StartPoint;
    this->Direction = 1;
    this->Speed = 20;
}

uint16_t CyclicVoltammetry::NextValue()
{
    active = true;
    this->PreviousValue = this->CurrentValue;
    if (Direction)
        this->CurrentValue += this->Speed;
    else
        this->CurrentValue -= this->Speed;

    if (this->CurrentValue >= this->FirstVertex)
    {
        this->CurrentValue = this->FirstVertex;
        this->Direction = false;
    }
    if (this->CurrentValue <= this->SecondVertex)
    {
        this->CurrentValue = this->SecondVertex;
        this->Direction = true;
    }

    if (this->CurrentValue == this->StartPoint)
        this->ZeroCrossNum--;
    else
    {
        if (((this->PreviousValue > this->StartPoint)
                && (this->StartPoint > this->CurrentValue))
                || ((this->CurrentValue > this->StartPoint)
                        && (this->StartPoint > this->PreviousValue)))
        {
            this->ZeroCrossNum--;
        }
    }

    if (this->ZeroCrossNum <= 0)
    {
        active = false;
    }
    return active;
}

uint16_t CyclicVoltammetry::getCurrentValue()
{
    return this->CurrentValue;
}

void CyclicVoltammetry::processData(char *data, int len)
{
    active = false;
    switch (data[0])
    {
    case StartMeasurement:
        active = true;
        break;
    case StoptMeasurement:
        active = false;
        break;
    case SetStartPoint:
        this->StartPoint = data[2];
        this->StartPoint = ((this->StartPoint << 6) & 0xFC0) | data[1];
        this->CurrentValue = this->StartPoint;
        break;
    case SetZeroCross:
        this->ZeroCrossNum = data[1];
        break;
    case SetFirstVertex:
        this->FirstVertex = data[2];
        this->FirstVertex = ((this->FirstVertex << 6) & 0xFC0) | data[1];
        break;
    case SetSecondVeretex:
        this->SecondVertex = data[2];
        this->SecondVertex = ((this->SecondVertex << 6) & 0xFC0) | data[1];
        break;
    case setSpeedVal:
        this->Speed = data[2];
        this->Speed = ((this->Speed << 6) & 0xFC0) | data[1];
        break;
    default:
        break;
    }
}

uint8_t CyclicVoltammetry::StopCondition()
{
    return this->ZeroCrossNum == 0;
}
