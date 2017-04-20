#include <stc89c5xrc.h>
#include <intrins.h>
#include <string.h>

#define FOSC 22118400L
#define BAUD 19200
#define P1_init ~0xFF

bit busy;
int flag=0;
int iloop=0;
char ram[10]=0;
char command=0;
int step_motor[8]={0x01,0x03,0x02,0x06,0x04,0x0c,0x08,0x09};

void SendData(unsigned char dat);
void SendString(char *s);
void terminal();
unsigned int strtonum(unsigned char inputstr);
void forward();
void back();
void delay();
void wait();

sbit ad=P2^1;
sbit su=P2^0;

void main()
{
    P1=P1_init;
    P2=0xFF;
    SCON = 0xda;
    TMOD = 0x20;
    ISP_CMD=0x00;
    ISP_CONTR|=0x81;
    ISP_TRIG=0x46;
    ISP_TRIG=0xb9;
    TH1 = TL1 = -(FOSC/12/32/BAUD);
    TR1 = 1;
    ES = 1;
    EA = 1;

    while(1)
	{
		terminal();
	}
}

void Uart_Isr() interrupt 4 using 1
{
    if (RI)
    {
        RI = 0;
        command=SBUF;
        flag=1;
    }
    if (TI)
    {
        TI = 0;
        busy=0;
    }
}

void SendData(unsigned char dat)
{
	while(busy)
    ACC = dat;
    if (P)
    {
        TB8 = 1;
    }
    else
    {
        TB8 = 0;
    }
	busy=1;
    SBUF = ACC;
}

void SendString(char *s)
{
    while (*s)
    {
        SendData(*s++);
    }
}

void terminal()
{
	char temp[2]=0;
    if(flag)
    {
        temp[0]=1;
        if(command=='R')
        {
            SendString("O");
        }
        else if(command == 'B')
        {
            EA=0;
			forward();
			EA=1;
        }
        else if(command == 'F')
        {
            EA=0;
            back();
            EA=1;
        }
        else if(command == 'A')
        {
            SendString("add\n");
            EA=0;
            ad=0;
            wait();
            ad=1;
            EA=1;
        }
        else if(command == 'S')
        {
            SendString("sub\n");
            EA=0;
            su=0;
            wait();
            su=1;
            EA=1;
        }
        else
        {
            ;
        }
        flag=0;
    }
}

void forward()
{
    int i,j;
    for(j=0;j<10;j++)
    for(i=0;i<8;i++)
    {
        P1=~step_motor[i];
        delay();
    }
    P1=P1_init;
}

void back()
{
    int i,j;
    for(j=0;j<10;j++)
    for(i=7;i>=0;i--)
    {
        P1=~step_motor[i];
        delay();
    }
    P1=P1_init;
}

void delay()  //1.5ms
{
	unsigned char i, j;

	i = 6;
	j = 93;
	do
	{
		while (--j);
	} while (--i);
}

void wait()	  //10ms
{
	unsigned char i, j;

	i = 18;
	j = 235;
	do
	{
		while (--j);
	} while (--i);
}


