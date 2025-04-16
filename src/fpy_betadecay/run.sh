# python main.py cumulative sample/conv-fpy_U235_JENDL4.0.dat > calc/u235_cm_jendl4.0.out
# python main.py cumulative sample/conv-fpy_U235_JENDL5.0.dat > calc/u235_cm_jendl5.0.out

# python main.py decayheat sample/conv-fpy_U235_JENDL4.0.dat > calc/u235_dh_jendl4.0.out
# python main.py decayheat sample/conv-fpy_U235_JENDL5.0.dat > calc/u235_dh_jendl5.0.out



python main.py -cumulative /Users/okumuras/Documents/calculations/talys/U235-en-allmodel/ffmodel1/yieldZA1.00E-06.fis > calc/u235_cm_low.out
python main.py -cumulative /Users/okumuras/Documents/calculations/talys/U235-en-allmodel/ffmodel1/yieldZA0001.000.fis > calc/u235_cm_1.0.out
python main.py -cumulative /Users/okumuras/Documents/calculations/talys/U235-en-allmodel/ffmodel1/yieldZA0003.000.fis > calc/u235_cm_3.0.out
python main.py -cumulative /Users/okumuras/Documents/calculations/talys/U235-en-allmodel/ffmodel1/yieldZA0005.000.fis > calc/u235_cm_5.0.out

# grep "40-Zr-95" u235*cm* | sed 's/u235_cm_//g' | sed 's/.out://g'  | sed 's/low/2.53E-8/' | sort -g > 40-Zr-95.cum
# grep "42-Mo-99" u235*cm* | sed 's/u235_cm_//g' | sed 's/.out://g'  | sed 's/low/2.53E-8/' | sort -g > 42-Mo-99.cum
# grep "56-Ba-140" u235*cm* | sed 's/u235_cm_//g' | sed 's/.out://g'  | sed 's/low/2.53E-8/' | sort -g > 56-Ba-140.cum
# grep "53-Ce-143" u235*cm* | sed 's/u235_cm_//g' | sed 's/.out://g'  | sed 's/low/2.53E-8/' | sort -g > 53-Ce-143.cum
# grep "60-Nd-147" u235*cm* | sed 's/u235_cm_//g' | sed 's/.out://g'  | sed 's/low/2.53E-8/' | sort -g > 60-Nd-147.cum



# python main.py decayheat /Users/okumuras/Documents/calculations/talys/U235-en-allmodel/ffmodel1/yieldZA1.00E-06.fis > calc/u235_dh_low.out
# python main.py decayheat /Users/okumuras/Documents/calculations/talys/U235-en-allmodel/ffmodel1/yieldZA0001.000.fis > calc/u235_dh_1.0.out
# python main.py decayheat /Users/okumuras/Documents/calculations/talys/U235-en-allmodel/ffmodel1/yieldZA0003.000.fis > calc/u235_dh_3.0.out
# python main.py decayheat /Users/okumuras/Documents/calculations/talys/U235-en-allmodel/ffmodel1/yieldZA0005.000.fis > calc/u235_dh_5.0.out



# python main.py cumulative /Users/sin/Documents/calculations/talys/aesj/Pu239_1.00E-6/yieldZA1.00E-06.fis > calc/pu239_cm_low.out
# python main.py cumulative /Users/sin/Documents/calculations/talys/aesj/Pu239_1.0/yieldZA0001.000.fis > calc/pu239_cm_1.0.out
# python main.py cumulative /Users/sin/Documents/calculations/talys/aesj/Pu239_3.0/yieldZA0003.000.fis > calc/pu239_cm_3.0.out
# python main.py cumulative /Users/sin/Documents/calculations/talys/aesj/Pu239_5.0/yieldZA0005.000.fis > calc/pu239_cm_5.0.out

# python main.py decayheat /Users/sin/Documents/calculations/talys/aesj/Pu239_1.00E-6/yieldZA1.00E-06.fis > calc/pu239_dh_low.out
# python main.py decayheat /Users/sin/Documents/calculations/talys/aesj/Pu239_1.0/yieldZA0001.000.fis > calc/pu239_dh_1.0.out
# python main.py decayheat /Users/sin/Documents/calculations/talys/aesj/Pu239_3.0/yieldZA0003.000.fis > calc/pu239_dh_3.0.out
# python main.py decayheat /Users/sin/Documents/calculations/talys/aesj/Pu239_5.0/yieldZA0005.000.fis > calc/pu239_dh_5.0.out


# grep "40-Zr-95" pu239*cm* | sed 's/pu239_cm_//g' | sed 's/.out://g'  | sed 's/low/2.53E-8/' | sort -g > Pu239-40-Zr-95.cum
# grep "42-Mo-99" pu239*cm* | sed 's/pu239_cm_//g' | sed 's/.out://g'  | sed 's/low/2.53E-8/' | sort -g > Pu239-42-Mo-99.cum
# grep "56-Ba-140" pu239*cm* | sed 's/pu239_cm_//g' | sed 's/.out://g'  | sed 's/low/2.53E-8/' | sort -g > Pu239-56-Ba-140.cum
# grep "53-Ce-143" pu239*cm* | sed 's/pu239_cm_//g' | sed 's/.out://g'  | sed 's/low/2.53E-8/' | sort -g > Pu239-53-Ce-143.cum
# grep "60-Nd-147" pu239*cm* | sed 's/pu239_cm_//g' | sed 's/.out://g'  | sed 's/low/2.53E-8/' | sort -g > Pu239-60-Nd-147.cum