/*
 * boardMSP.cpp
 *
 *  Created on: Mar 11, 2020
 *      Author: killan
 */

#include <boardMSP.h>


void initTimer_A(void)
{    //Timer Configuration
    TA0CCR0 = 0; //Initially, Stop the Timer
    TA0CCTL0 |= CCIE; //Enable interrupt for CCR0.
    TA0CTL = TASSEL_2 + ID_3 + MC_3; //Select SMCLK, SMCLK/8 , Up DOWN Mode
}

int board_init()
{
    /* Disable Watchdog */
    WDTCTL = WDTPW + WDTHOLD; //Stop watchdog timer

    // Clear DCO
    DCOCTL = 0;
    /* Configure 16MHz Clock */
    BCSCTL1 = CALBC1_16MHZ;
    DCOCTL = CALDCO_16MHZ;

    /* Configure Pin */
    GPIO::setBit(&P2DIR, 0xFF);
    GPIO::clearBit(&P2SEL, 0xFF);
    GPIO::clearBit(&P2SEL2, 0xFF);
    GPIO::setBit(&P1DIR, (BIT4 + BIT5 + BIT6 + BIT7));
    GPIO::clearBit(&P1SEL, (BIT4 + BIT5 + BIT6 + BIT7));
    GPIO::clearBit(&P1SEL2, (BIT4 + BIT5 + BIT6 + BIT7));

    /* initialize modules */
    /* Enable USCI_A0 RX interrupt */
    IE2 |= UCA0RXIE;
    /* Global interrupt  */
    __enable_interrupt();

    return 0;
}

// ADC10 interrupt service routine
#pragma vector = ADC10_VECTOR
__interrupt void ADC10_ISR(void)
{
    __bic_SR_register_on_exit(CPUOFF);        // Return to active mode }
}
