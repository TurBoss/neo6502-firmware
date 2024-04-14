; ************************************************************************************************
; ************************************************************************************************
;
;		Name:		operands.asm
;		Purpose:	Operands handling
;		Created:	9th April 2024
;		Reviewed: 	No
;		Author:		Paul Robson (paul@robsons.org.uk)
;
; ************************************************************************************************
; ************************************************************************************************

		.section 	code

; ************************************************************************************************
;
;									Get a single register to A
;
; ************************************************************************************************

SweetAsmGetRegister:
		jsr 	EXPEvalInteger8
		cmp 	#16
		bcs 	_SAGRRange
		rts
_SAGRRange:
		.error_range		

; ************************************************************************************************
;
;								Get a single register to A n or @an
;
; ************************************************************************************************

SweetAsmGetAltRegister:
		lda 	(codePtr),y 				; check @x
		cmp 	#KWD_AT
		bne 	SweetAsmGetRegister  		; just normal register

		iny 								; consume @
		jsr 	SweetAsmGetRegister 		; get register
		ora 	#$20 						; indirect adjust
		rts

		.send 	code

; ************************************************************************************************
;
;									Changes and Updates
;
; ************************************************************************************************
;
;		Date			Notes
;		==== 			=====
;
; ************************************************************************************************