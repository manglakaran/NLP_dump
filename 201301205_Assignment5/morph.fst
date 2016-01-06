$kaagaz-morph$ = <Noun>:<> ({<singular><direct>}:{} | {<singular><oblique>}:{} |{<plural><direct>}:{} | {<plural><oblique>}:{oM})

$beta-morph$ = <Noun>:<> ({<singular><direct>}:{} | {<singular><oblique>}:{e} |{<plural><direct>}:{e} | {<plural><oblique>}:{oM})

$baat-morph$ = <Noun>:<> ({<singular><direct>}:{} | {<singular><oblique>}:{} |{<plural><direct>}:{eN} | {<plural><oblique>}:{oM})

$hindi-morph$ = <Noun>:<> ({<singular><direct>}:{} | {<singular><oblique>}:{} | {<plural><direct>}:{} | {<plural><oblique>}:{})

$rAjA-morph$ = <Noun>:<> ({<singular><direct>}:{} | {<singular><oblique>}:{} |{<plural><direct>}:{} | {<plural><oblique>}:{oM})

$vAyu-morph$ = <Noun>:<> ({<singular><direct>}:{} | {<singular><oblique>}:{} | {<plural><direct>}:{} | {<plural><oblique>}:{})

$agni-morph$ = <Noun>:<> ({<singular><direct>}:{} | {<singular><oblique>}:{} | {<plural><direct>}:{} | {<plural><oblique>}:{})

$morph$ = "kaagaz-paradigm.lex" $kaagaz-morph$ | "beta-paradigm.lex" $beta-morph$ | "baat-paradigm.lex" $baat-morph$ | "hindi-paradigm.lex" $hindi-morph$ | "rAjA-paradigm.lex" $rAjA-morph$ | "agni-paradigm.lex" $agni-morph$ | "vAyu-paradigm.lex" $vAyu-morph$



ALPHABET = [A-Za-z] [<Noun> A e oM]:<>
$delete-A$ = [e oM] <=> <> (<Noun>:<>[e oM])

ALPHABET = [A-Za-z] [<Noun> a e oM]:<>
$delete-a$ = [e oM] <=> <> (<Noun>:<>[e oM])

$morph$ || $delete-A$ || $delete-a$
