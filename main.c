/*
 * ComunicacionSerial.c
 *
 * Created: 31/7/2021 22:33:12
 * Author : Carlos Rodriguez Lema
 */ 

#define F_CPU 16000000UL
#include <avr/io.h>
#include <avr/interrupt.h>
#include "UART.h"
#include <util/delay.h>

ISR(INT0_vect){
	PORTC |= (1<<0);
	UART_init();
	UART_write_txt("Bienvenido \n\r");
		
	uint8_t dato = 0;
	int control;
	control = 0;
	while (control == 0){
		dato = UART_read();
		if(dato != 0){
			switch(dato){
				case 'e':
				UART_write_txt("Alzando baranda \n\r");
				int abr;
				abr = 0;
				int cer;
				cer = 0;
				
				while (abr <= 250){
					abr = abr + 1;
					PORTB |= (1<<PORTB0);
					PORTB &=~ (1<<PORTB1);
					PORTB &=~ (1<<PORTB2);
					PORTB &=~ (1<<PORTB3);
					_delay_ms(2);
					PORTB &=~ (1<<PORTB0);
					PORTB |= (1<<PORTB1);
					PORTB &=~ (1<<PORTB2);
					PORTB &=~ (1<<PORTB3);
					_delay_ms(2);
					PORTB &=~ (1<<PORTB0);
					PORTB &=~ (1<<PORTB1);
					PORTB |= (1<<PORTB2);
					PORTB &=~ (1<<PORTB3);
					_delay_ms(2);
					PORTB &=~ (1<<PORTB0);
					PORTB &=~ (1<<PORTB1);
					PORTB &=~ (1<<PORTB2);
					PORTB |= (1<<PORTB3);
					_delay_ms(2);
				}
				
				UART_write_txt("Ingrese por favor \n\r");
				_delay_ms(5000);
				
				while (cer <= 250){
					cer = cer + 1;
					PORTB &=~ (1<<PORTB0);
					PORTB &=~ (1<<PORTB1);
					PORTB &=~ (1<<PORTB2);
					PORTB |= (1<<PORTB3);
					_delay_ms(2);
					PORTB &=~ (1<<PORTB0);
					PORTB &=~ (1<<PORTB1);
					PORTB |= (1<<PORTB2);
					PORTB &=~ (1<<PORTB3);
					_delay_ms(2);
					PORTB &=~ (1<<PORTB0);
					PORTB |= (1<<PORTB1);
					PORTB &=~ (1<<PORTB2);
					PORTB &=~ (1<<PORTB3);
					_delay_ms(2);
					PORTB |= (1<<PORTB0);
					PORTB &=~ (1<<PORTB1);
					PORTB &=~ (1<<PORTB2);
					PORTB &=~ (1<<PORTB3);
					_delay_ms(2);
				}
			}
		control = 1;
		}
	PORTB &=~ (1<<PORTB0);
	PORTB &=~ (1<<PORTB1);
	PORTB &=~ (1<<PORTB2);
	PORTB &=~ (1<<PORTB3);
	}
}

ISR(INT1_vect){
	PORTC |= (1<<0);
	UART_init();
	UART_write_txt("Gracias por su visita y por usar APParquear \n\r");
	
	uint8_t dato = 0;
	int control;
	control = 0;
	while (control == 0){
		dato = UART_read();
		if(dato != 0){
			switch(dato){
				case 's':
				UART_write_txt("Alzando baranda \n\r");
				int abr;
				abr = 0;
				int cer;
				cer = 0;
				
				while (abr <= 250){
					abr = abr + 1;
					PORTB |= (1<<PORTB0);
					PORTB &=~ (1<<PORTB1);
					PORTB &=~ (1<<PORTB2);
					PORTB &=~ (1<<PORTB3);
					_delay_ms(2);
					PORTB &=~ (1<<PORTB0);
					PORTB |= (1<<PORTB1);
					PORTB &=~ (1<<PORTB2);
					PORTB &=~ (1<<PORTB3);
					_delay_ms(2);
					PORTB &=~ (1<<PORTB0);
					PORTB &=~ (1<<PORTB1);
					PORTB |= (1<<PORTB2);
					PORTB &=~ (1<<PORTB3);
					_delay_ms(2);
					PORTB &=~ (1<<PORTB0);
					PORTB &=~ (1<<PORTB1);
					PORTB &=~ (1<<PORTB2);
					PORTB |= (1<<PORTB3);
					_delay_ms(2);
				}
				
				UART_write_txt("Salga por favor \n\r");
				_delay_ms(5000);
				
				while (cer <= 250){
					cer = cer + 1;
					PORTB &=~ (1<<PORTB0);
					PORTB &=~ (1<<PORTB1);
					PORTB &=~ (1<<PORTB2);
					PORTB |= (1<<PORTB3);
					_delay_ms(2);
					PORTB &=~ (1<<PORTB0);
					PORTB &=~ (1<<PORTB1);
					PORTB |= (1<<PORTB2);
					PORTB &=~ (1<<PORTB3);
					_delay_ms(2);
					PORTB &=~ (1<<PORTB0);
					PORTB |= (1<<PORTB1);
					PORTB &=~ (1<<PORTB2);
					PORTB &=~ (1<<PORTB3);
					_delay_ms(2);
					PORTB |= (1<<PORTB0);
					PORTB &=~ (1<<PORTB1);
					PORTB &=~ (1<<PORTB2);
					PORTB &=~ (1<<PORTB3);
					_delay_ms(2);
				}
			}
		control = 1;
		}
	PORTB &=~ (1<<PORTB0);
	PORTB &=~ (1<<PORTB1);
	PORTB &=~ (1<<PORTB2);
	PORTB &=~ (1<<PORTB3);
	}
}

int main(void)
{
	//Salida para los motores
	DDRB |= (1<<DDB0); //BIT 2 3 4 OUTPUT
	DDRB |= (1<<DDB1);
	DDRB |= (1<<DDB2);
	DDRB |= (1<<DDB3);
	
	PORTB &=~ (1<<PORTB0);
	PORTB &=~ (1<<PORTB1);
	PORTB &=~ (1<<PORTB2);
	PORTB &=~ (1<<PORTB3);
	
	//Configuramos las interrupciones	
	DDRC |= (1<<0);			// Definimos al pin C0 como salida
	PORTC &=~ (1<<0);
	
	DDRD &=~ (1<<2);		//Interrupcion como entrada
	PORTD |= (1<<2);
	
	DDRD &=~ (1<<3);		//Interrupcion como entrada
	PORTD |= (1<<3);
	
	EICRA = 0b00001010;
	EIMSK = 0b00000011;
	EIFR = 0b00000000;
	
	sei();
	
	while (1){
		PORTC |= (1<<0);
		_delay_ms(250);
		PORTC &=~ (1<<0);
		_delay_ms(250);
	}
}
