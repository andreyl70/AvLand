#encoding "utf-8"
#GRAMMAR_ROOT S

#include <../main.cxx>

GorSokr -> "г" (Punct) | "гор" (Punct);
DerevnyaSokr  -> "д" (Punct) | "дер" (Punct);
RaionSokr -> "р-н" (Punct) | "р-на";

RaionPred -> RaionSokr | "район";
Raion -> Adj<kwtype="район", gnc-agr[1]> interp (Place.Raion) RaionPred<gnc-agr[1],rt>;
S -> Raion;

DerevnyaPred -> DerevnyaSokr | "деревня";
Derevnya -> DerevnyaPred<rt> Word<kwtype="деревня", h-reg1> interp (Place.Derevnya);
S -> Derevnya;

Km -> "км" (Punct) | "километр";
S -> Val interp (Distance.ValKm) Km "от" Word<kwtype="деревня", h-reg1> interp (Distance.Point);

