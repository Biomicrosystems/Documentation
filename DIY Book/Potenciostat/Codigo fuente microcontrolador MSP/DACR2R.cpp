/*
 * DACR2R.cpp
 *
 *  Created on: Mar 11, 2020
 *      Author: killan
 */

#include <DACR2R.h>

DAC_R2R::DAC_R2R()
{
    /* Initialize default Values */
}

int DAC_R2R::setValue(int16_t value)
{
    P1OUT = ((value >> 4) & 0xF0);
    P2OUT = (value & 0xFF);
    return 0;
}
