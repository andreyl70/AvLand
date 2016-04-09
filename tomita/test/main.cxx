#encoding "utf-8"

Val -> AnyWord<wff=/\d+/>;
WordList  -> AnyWord+;
ValList   -> Val+;

//City -> Adj<gnc-agr[1], h-reg1>* Noun<rt, gnc-agr[1], h-reg1>+;
//S -> "участок" Val interp (Debug.Item1)
//     "сот" interp (Debug.Item2) (Punct)
//     (WordList) "в" City interp (Debug.Item3);
//
//S -> ValList interp (Debug.Item1) "руб" Punct;
//
//
//S -> Adj<gnc-agr[1], h-reg1>* interp (Debug.Item2) "область"<gnc-agr[1], rt>;
