

src_train="mydata/en-US.train.txt"
src_dev="mydata/en-US.dev.txt"
src_test="mydata/en-US.test.txt"
tgt_train="mydata/zh-CN.train.txt"
tgt_dev="mydata/zh-CN.dev.txt"
tgt_test="mydata/zh-CN.test.txt"

save_data=mydata/datafull
save_model=mydata/modelfull

echo "tokenize"
th tools/tokenize.lua -joiner_annotate -case_feature < ${src_train} > ${src_train}.tok
th tools/tokenize.lua -joiner_annotate -case_feature < ${src_dev} > ${src_dev}.tok
th tools/tokenize.lua -joiner_annotate -case_feature < ${src_test} > ${src_test}.tok
th tools/tokenize.lua -joiner_annotate < ${tgt_train} > ${tgt_train}.tok
th tools/tokenize.lua -joiner_annotate < ${tgt_dev} > ${tgt_dev}.tok
th tools/tokenize.lua -joiner_annotate < ${tgt_test} > ${tgt_test}.tok

echo "preprocessing"
th preprocess.lua -train_src ${src_train}.tok -train_tgt ${tgt_train}.tok -valid_src ${src_dev}.tok -valid_tgt ${tgt_dev}.tok -save_data ${save_data} 

echo "train"
th train.lua -data ${save_data}-train.t7 -save_model ${save_model} -gpuid 1

cp -f mydata/${save_model}"_epoch13_"*".t7" mydata/${save_model}"_final.t7"

echo "test"
th translate.lua -model ${save_model}_final.t7 -src ${src_test}.tok -output ${tgt_test}.out.tok -gpuid 1

echo "evaluate"
th tools/detokenize.lua  < ${tgt_test}.out.tok  > ${tgt_test}.out.detok
perl multi-bleu.perl ${tgt_test} < ${tgt_test}.out.detok > ${tgt_test}.bleu.txt

