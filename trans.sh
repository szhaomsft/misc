
infile=$1



th tools/tokenize.lua -joiner_annotate -case_feature < ${infile} > ${infile}.tok


th translate.lua  -replace_unk  -model mydata/modelfull_final_cpu.t7 -src ${infile}.tok -output ${infile}.out.tok
