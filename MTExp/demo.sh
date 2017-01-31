

src_train="mydata/Bi-Education.txt.en-US.train"
src_dev="mydata/Bi-Education.txt.en-US.dev"
src_test="mydata/Bi-Education.txt.en-US.test"
tgt_train="mydata/Bi-Education.txt.zh-CN.train"
tgt_dev="mydata/Bi-Education.txt.zh-CN.dev"
tgt_test="mydata/Bi-Education.txt.zh-CN.test"

save_data=mydata/data
save_model=mydata/model

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
th translate.lua  -replace_unk  -model ${save_model}_final.t7 -src ${src_test}.tok -output ${tgt_test}.out.tok -gpuid 1

echo "evaluate"

th tools/detokenize.lua  < ${tgt_test}.out.tok  > ${tgt_test}.out.detok
perl multi-bleu.perl ${tgt_test} < ${tgt_test}.out.detok > ${tgt_test}.bleu.txt

echo "convert model to cpu"
th tools/release_model.lua -force -model ${save_model}_final.t7   -output_model${save_model}_final_cpu.t7  -gpuid 1
