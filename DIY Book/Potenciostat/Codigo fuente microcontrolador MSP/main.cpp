#include <msp430.h>
#include <GPIO.h>
#include <CyclicVoltammetry.h>
#include <ASV.h>
#include <SWASV.h>
#include <DACR2R.h>
#include <boardMSP.h>
#include <ADC.h>

/**
 * main.cpp
 */

using namespace msp;

enum seltech
{
    CVTech = 0xC0, ASTech = 0xC1, SWASVTech = 0xC2
};

Technique *medidas[] = { new CyclicVoltammetry(), new ASV(), new SWASV() };

uart serial;
ADC analog;

#define DEVICE_ID 0xA0
#define DEVICE_END 0xAB

unsigned int SelectedTechnique = 0;

uint16_t ADC_data = 0;
uint8_t data_send[4] = { 0, 0, 0, 0 };

unsigned char dato1, dato2;

char data[4];
uint16_t complete;

unsigned int i = 0;

int main(void)
{
    if (board_init() == 0)
    {
        if (serial.init(115200) == 0)
        {
            if (analog.init(BIT0 + BIT3) == 0)
            {
                // Init modules
                initTimer_A();
                TA0CCR0 = 50000 - 1; //Start Timer, Compare value for Up Mode to get 1ms delay per loop
                /* Enable USCI_A0 RX interrupt */
                IE2 |= UCA0RXIE;
                // Clear the timer and enable timer interrupt
                __enable_interrupt();
                /* LPM0 with interrupts enabled */
                __bis_SR_register(LPM0 + GIE);
                for (;;)
                {
                }
            }
        }
    }
    return 0;
}

#pragma vector=USCIAB0RX_VECTOR
__interrupt void USCI0RX_ISR(void)
{
    switch (UCA0RXBUF)
    {
    case StartID: //Inicio de Trama
        i = 0;
        break;
    case CVTech:
        SelectedTechnique = 0;
        i = 0;
        break;
    case ASTech:
        SelectedTechnique = 1;
        break;
    case SWASVTech:
        SelectedTechnique = 2;
        break;
    case EndPKG: //Fin de Trama
        medidas[SelectedTechnique]->processData(data, i);
        break;
    default:
        data[i] = UCA0RXBUF;
        i++;
        if (i >= 5)
            i = 0;
        break;
    }
}

uint16_t nextval;
// Timer A0 Interrupt Service Routine
#pragma vector = TIMER0_A0_VECTOR
__interrupt void Timer_A_CCR0_ISR(void)
{
    if (medidas[SelectedTechnique]->isRunning())
    {
        nextval = medidas[SelectedTechnique]->getCurrentValue();

        medidas[SelectedTechnique]->dac->setValue(nextval);

        //ADC_data = analog.readSingleChannel(0);
        ADC_data = nextval;
        data_send[0] = (0x3F & (ADC_data >> 6));
        data_send[1] = (0x3F & ADC_data);
        ADC_data = analog.readSingleChannel(3);
        data_send[2] = (0x3F & (ADC_data >> 6));
        data_send[3] = (0x3F & ADC_data);

        serial.putchar(StartID);
        serial.putchar(data_send[0]);
        serial.putchar(data_send[1]);
        serial.putchar(data_send[2]);
        serial.putchar(data_send[3]);
        medidas[SelectedTechnique]->NextValue();
    }
    else
    {
        if (medidas[SelectedTechnique]->StopCondition())
        {
            serial.putchar(ACK);
            serial.putchar(ENDRUN);
        }
    }
}

