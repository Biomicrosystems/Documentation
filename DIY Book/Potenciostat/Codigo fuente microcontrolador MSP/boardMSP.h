/*
 * board.h
 *
 *  Created on: Mar 11, 2020
 *      Author: killan
 */

#ifndef BOARDMSP_H_
#define BOARDMSP_H_

#include <msp430.h>
#include <GPIO.h>
#include <uart.h>

using namespace msp;

enum Commands
{
    StartID = 0xA0,
    EndPKG = 0xAB,
    StartMeasurement = 0x01,
    StoptMeasurement = 0x02,
    SetStartPoint = 0x03,
    SetZeroCross = 0x04,
    SetFirstVertex = 0x05,
    SetSecondVeretex = 0x06,
    setSpeedVal = 0x07,
    SetTimeHold = 0x11,
    SetFinalValue= 0x12,
    ACK = 0xB0,
    ENDRUN = 0xB1
};

void initTimer_A(void);

int board_init();



#endif /* BOARDMSP_H_ */
