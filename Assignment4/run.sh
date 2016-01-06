echo "Running for HINDI"
python matrix_builder.py HINDI
python smoother.py HINDI 0.5 0.1
python viterbi_decoder.py HINDI > final_output_HINDI
python test.py
