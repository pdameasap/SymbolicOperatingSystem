(* versare_syntax.v *)

Require Import Coq.Strings.String.
Require Import Coq.Lists.List.
Import ListNotations.

Module rocq.
Module rocq.versare_syntax.

(* === Emoji inventory === *)
Inductive emoji : Type :=
  | EmojiLove
  | EmojiSad
  (* TODO: extend with your full emoji set *)
  .

(* === Z‑Glyph Primes === *)
Inductive Zglyph : Type :=
  | Z1  | Z2  | Z3  | Z4  | Z5  | Z6  | Z7  | Z8  | Z9
  | Z10 | Z11 | Z12 | Z13 | Z14 | Z15 | Z16 | Z17 | Z18.

(* === Noun lexicon === *)
Inductive noun : Type :=
  (* TODO: replace these stubs with your ~200 nouns *)
  | N_Ocean
  | N_Heart
  .

(* === Core AST === *)
Inductive expr : Type :=
  | EClause  (subj : noun) (pred : list Zglyph) (mod : option emoji)
  | EDefine  (name : string) (body : expr)
  | EInvoke  (name : string)
  | EIf      (cond then_br : expr)
  | EEval    (z : Zglyph) (body : expr)
  | ECall    (fname : string) (args : list expr)
  .

End versare_syntax.
End rocq.

Export rocq.versare_syntax.
