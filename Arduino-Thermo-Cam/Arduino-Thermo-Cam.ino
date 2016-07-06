// ====================================================================
#define R_0 11
#define R_1 12
#define R_2 13

#define NUM_IR 12

int DATA_0[NUM_IR];
int DATA_1[NUM_IR];
int DATA_2[NUM_IR];

int AN[] = {
    // Normal
    // A0, A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11

    // Reversed
    A11, A10, A9, A8, A7, A6, A5, A4, A3, A2, A1, A0
};

//unsigned int mSerialSpeed = 9600;
//unsigned int mSerialSpeed = 19200;
unsigned int mSerialSpeed = 57600;

// ====================================================================
int STP_DELAY = 5;

int SMP_A = 22;
int SMP_B = 23;
int SMP_C = 24;
int SMP_D = 25;

int HEAD_DIR = 1;

int HEAD_CURR_POS = 30;
int HEAD_MAX_POS = 60;
int HEAD_MIN_POS = 0;


// ====================================================================
void print( String data )   { Serial.print( data ); }
void println( String data ) { Serial.println( data ); }

void print( int data )   { Serial.print( data ); }
void println( int data ) { Serial.println( data ); }

// ====================================================================
void POWER_OFF(void) {
    digitalWrite( R_0, LOW);
    digitalWrite( R_1, LOW);
    digitalWrite( R_2, LOW);
}

// ====================================================================
int MAX_VAL = 1000;
int MIN_VAL = 0;
int TO_VAL  = 255;

String DATA_OUT = "";
int ROW = 30;
int RAW_VAL = 0;

bool USER_ONE_FOR_ALL = false;

void READ_ROWS() {

    // ------------------------------------------------------------
    DATA_OUT = String(ROW)+"|";

    // ------------------------------------------------------------
    if ( USER_ONE_FOR_ALL ) {

        // ------------------------------------------------------------
        POWER_OFF();
        digitalWrite( R_2, HIGH);

        for (int i=0; i < NUM_IR; i++) {
            RAW_VAL = map( MAX_VAL-analogRead( AN[i] ), 0, MAX_VAL, 0, TO_VAL );
            if (RAW_VAL < 0) {
                DATA_2[i] = 0;
                DATA_OUT += "0,0,0,";
            } else {

                DATA_2[i] = RAW_VAL;

                if (RAW_VAL > 20) {

                    if ( i > 0 && i < NUM_IR-1 ) {


                        if (DATA_2[i-1] > DATA_2[i]) {
                            DATA_OUT += String(RAW_VAL+20)+","+String(RAW_VAL)+","+String(RAW_VAL-20)+",";

                        } else if (DATA_2[i-1] < DATA_2[i]) {
                            DATA_OUT += String(RAW_VAL-20)+","+String(RAW_VAL)+","+String(RAW_VAL+20)+",";

                        } else {
                            DATA_OUT += String(RAW_VAL)+","+String(RAW_VAL)+","+String(RAW_VAL)+",";
                        }


                    } else {
                        DATA_OUT += String(RAW_VAL-20)+","+String(RAW_VAL)+","+String(RAW_VAL-20)+",";

                    }

                } else {
                    DATA_OUT += String(RAW_VAL)+","+String(RAW_VAL)+","+String(RAW_VAL)+",";
                }

            }
        }

        // ------------------------------------------------------------

    } else {

        // ------------------------------------------------------------
        POWER_OFF();
        digitalWrite( R_0, HIGH);

        for (int i=0; i < NUM_IR; i++) {

            RAW_VAL = map( MAX_VAL-analogRead( AN[i] ), 0, MAX_VAL, 0, TO_VAL );
            if (RAW_VAL < 0) {
                //DATA_0[i] = 0;
                DATA_OUT += "0,";
            } else {

                //DATA_0[i] = RAW_VAL;
                DATA_OUT += String(RAW_VAL)+",";
            }

        }

        // ------------------------------------------------------------
        POWER_OFF();
        digitalWrite( R_1, HIGH);

        for (int i=0; i < NUM_IR; i++) {

            RAW_VAL = map( MAX_VAL-analogRead( AN[i] ), 0, MAX_VAL, 0, TO_VAL );
            if (RAW_VAL < 0) {
                //DATA_1[i] = 0;
                DATA_OUT += "0,";

            } else {
                //DATA_1[i] = RAW_VAL;
                DATA_OUT += String(RAW_VAL)+",";
            }

        }

        // ------------------------------------------------------------
        POWER_OFF();
        digitalWrite( R_2, HIGH);

        for (int i=0; i < NUM_IR; i++) {
            RAW_VAL = map( MAX_VAL-analogRead( AN[i] ), 0, MAX_VAL, 0, TO_VAL );

            if (RAW_VAL < 0) {
                DATA_OUT += "0,";
                //DATA_2[i] = 0;
            } else {
                DATA_OUT += String(RAW_VAL)+",";
                //DATA_2[i] = RAW_VAL;

            }
        }
        // ------------------------------------------------------------

    }

    // ------------------------------------------------------------
    Serial.print( DATA_OUT+"\n" );
    // ------------------------------------------------------------

}

// ====================================================================
void setup(void) {

    // ------------------------------------------------------------
    Serial.begin( mSerialSpeed);

    for (int i=0; i < NUM_IR; i++) pinMode( AN[i] , INPUT);

    pinMode( R_0, OUTPUT);
    pinMode( R_1, OUTPUT);
    pinMode( R_2, OUTPUT);

    POWER_OFF();

    pinMode( SMP_A, OUTPUT); pinMode( SMP_B, OUTPUT); pinMode( SMP_C, OUTPUT); pinMode( SMP_D, OUTPUT);

    SM_CLEAR(SMP_A, SMP_B, SMP_C, SMP_D);
    // ------------------------------------------------------------

}

// ====================================================================
bool ALLOW_RUN = false;

void loop( void ) {

    // ALLOW scan head to go in middle point (HEAD_MAX_POS/2 == 30)
    if (
        (!ALLOW_RUN)
        &&
        (HEAD_CURR_POS == HEAD_MAX_POS/2)
    ) {

        delay(100);
        digitalWrite( R_0, LOW);
        digitalWrite( R_1, LOW);
        digitalWrite( R_2, LOW);
        return;

    }

    // ------------------------------------------------------------
    if ( HEAD_DIR == 1 ) {

        if ( HEAD_CURR_POS < HEAD_MAX_POS) {
            HEAD_CURR_POS++;

        } else {
            HEAD_CURR_POS--;
            HEAD_DIR = 0;
        }

    } else {

        if ( HEAD_CURR_POS > HEAD_MIN_POS) {
            HEAD_CURR_POS--;

        } else {
            HEAD_CURR_POS++;
            HEAD_DIR = 1;
        }

    }

    ROW = HEAD_MAX_POS-HEAD_CURR_POS;

    // ------------------------------------------------------------
    READ_ROWS();
    SM_MK_STEM( SMP_A, SMP_B, SMP_C, SMP_D, 0, HEAD_DIR);

    SM_CLEAR(SMP_A, SMP_B, SMP_C, SMP_D);
    delay(10);
    // ------------------------------------------------------------

}

// ====================================================================
String _str_act,_ACT, _ACT_DATA = "";

void serialEvent() {

    // ------------------------------------------------------------
    while (Serial.available() > 0 ) {
        _str_act = Serial.readString();
    }
    _ACT = _str_act.substring(0, _str_act.indexOf(","));
    _ACT_DATA = _str_act.substring(_str_act.indexOf(",")+1);
    // --------------------------------------------------------
    int _valid_cmd = 0;
    // --------------------------------------------------------
    if (_ACT == "start") {
        ALLOW_RUN = true;

    } else if (_ACT == "stop") {
        ALLOW_RUN = false;

    } else if (_ACT == "head_up") {
        if ( !ALLOW_RUN ) {

            for (int i=0; i < _ACT_DATA.toInt(); i++ )
                SM_MK_STEM( SMP_A, SMP_B, SMP_C, SMP_D, 0, 1);

            SM_CLEAR(SMP_A, SMP_B, SMP_C, SMP_D);

        }

    } else if (_ACT == "head_down") {
        if ( !ALLOW_RUN ) {

            for (int i=0; i < _ACT_DATA.toInt(); i++ )
                SM_MK_STEM( SMP_A, SMP_B, SMP_C, SMP_D, 0, 0);

            SM_CLEAR(SMP_A, SMP_B, SMP_C, SMP_D);

        }

    }

    // ------------------------------------------------------------
}

// ====================================================================
void SM_MK_STEM(int p1, int p2, int p3, int p4, int type, int SIDE) {

    int t1, t2, t3, t4;

    if (SIDE == 1) {
        t1 = p1; t2 = p2; t3 = p3; t4 = p4;
    } else {
        t1 = p4; t2 = p3; t3 = p2; t4 = p1;
    }

    if (type == 0) {
        /*  LOW TURQUE  */
        digitalWrite(t1, HIGH); digitalWrite(t2, LOW); digitalWrite(t3, LOW); digitalWrite(t4, LOW); delay(STP_DELAY);
        digitalWrite(t1, LOW); digitalWrite(t2, HIGH); digitalWrite(t3, LOW); digitalWrite(t4, LOW); delay(STP_DELAY);
        digitalWrite(t1, LOW); digitalWrite(t2, LOW); digitalWrite(t3, HIGH); digitalWrite(t4, LOW); delay(STP_DELAY);
        digitalWrite(t1, LOW); digitalWrite(t2, LOW); digitalWrite(t3, LOW); digitalWrite(t4, HIGH); delay(STP_DELAY);
    } else if (type == 1) {
        /*  HIGH TURQUE  */
        digitalWrite(t1, HIGH); digitalWrite(t2, HIGH); digitalWrite(t3, LOW); digitalWrite(t4, LOW); delay(STP_DELAY);
        digitalWrite(t1, LOW); digitalWrite(t2, HIGH); digitalWrite(t3, HIGH); digitalWrite(t4, LOW); delay(STP_DELAY);
        digitalWrite(t1, LOW); digitalWrite(t2, LOW); digitalWrite(t3, HIGH); digitalWrite(t4, HIGH); delay(STP_DELAY);
        digitalWrite(t1, HIGH); digitalWrite(t2, LOW); digitalWrite(t3, LOW); digitalWrite(t4, HIGH); delay(STP_DELAY);
    }

}
// ====================================================================
void SM_CLEAR(int p1, int p2, int p3, int p4) {
    digitalWrite(p1, LOW); digitalWrite(p2, LOW); digitalWrite(p3, LOW); digitalWrite(p4, LOW);

}

// ====================================================================
void SM_LOCK_HIGH(int p1, int p2, int p3, int p4) {
    digitalWrite(p1, HIGH); digitalWrite(p2, HIGH); digitalWrite(p3, LOW); digitalWrite(p4, LOW);
}

// ====================================================================
void SM_LOCK_LOW(int p1, int p2, int p3, int p4) {
    digitalWrite(p1, HIGH); digitalWrite(p2, LOW); digitalWrite(p3, LOW); digitalWrite(p4, LOW);
}
// ====================================================================







