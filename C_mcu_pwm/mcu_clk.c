#include <reg51.h>
#include <intrins.h>
#define step 1
#define all 333

int pwm;
sbit out=P1^0;
sbit ad=P2^1;
sbit su=P2^0;

void delay();

int main()
{
    int i;

    pwm=all/2;

    P2=0xFF;
    P1=0x00;
    out=1;
    delay();
    out=0;
    while(1)
    {
        if(~ad&&(pwm<all-step))
            pwm+=step;
        out=1;
        for(i=0;i<pwm;i++)
            ;
        if(~su&&(pwm>=step))
            pwm-=step;
        out=0;
        for(i=0;i<(all-pwm);i++)
            ;
    }
}

void delay() //1s
{
	unsigned char i, j, k;

	_nop_();
	i = 15;
	j = 2;
	k = 235;
	do
	{
		do
		{
			while (--k);
		} while (--j);
	} while (--i);
}
