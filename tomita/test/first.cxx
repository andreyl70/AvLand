#encoding "utf-8"
#GRAMMAR_ROOT S

Val       -> AnyWord<wff=/\d+/>;
City      -> Adj<gnc-agr[1], h-reg1>* Noun<rt, gnc-agr[1], h-reg1>+;

DerevnyaPred  -> "деревня" | "д" (Punct) | "дер" (Punct);
Derevnya -> DerevnyaPred Word<h-reg1>+ interp (Debug.Item1);

Raion     -> Adj<gnc-agr[1], h-reg1> interp (Debug.Item2) "район"<gnc-agr[1], rt>;

ShosseDist -> ValList interp (Debug.Item3) "км" (Punct);
ShosseName -> Adj<gnc-agr[1]> interp (Debug.Item4) "шоссе"<gnc-agr[1], rt>;
Shosse    ->  ShosseDist ShosseName;

WordList  -> AnyWord+;
ValList   -> Val+;

S -> "участок" Val interp (Debug.Item1)
     "сот" interp (Debug.Item2) (Punct)
     (WordList) "в" City interp (Debug.Item3);

S -> ValList interp (Debug.Item1) "руб" Punct;

S -> "в" Derevnya Raion (Comma) Shosse;

