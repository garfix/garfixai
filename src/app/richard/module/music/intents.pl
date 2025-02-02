intent_play_music(A) :- play_music(A), store(output_type('ok')).
intent_stop_music(A) :- stop_music(), store(output_type('ok')).
