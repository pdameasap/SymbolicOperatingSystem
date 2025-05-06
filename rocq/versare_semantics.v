(* versare_semantics.v *)

Require Import Coq.Init.Nat.
Require Import Coq.Lists.List.
Import ListNotations.
Require Import versare_syntax.

(* --- A simple numeric domain for Z-axis weights --- *)
Record zvector : Type := {
  z1v  : nat; z2v  : nat; z3v  : nat; z4v  : nat; z5v  : nat;
  z6v  : nat; z7v  : nat; z8v  : nat; z9v  : nat; z10v : nat;
  z11v : nat; z12v : nat; z13v : nat; z14v : nat; z15v : nat;
  z16v : nat; z17v : nat; z18v : nat
}.

(* The “zero” vector *)
Definition default_zvector : zvector := {|
  z1v  := 0;  z2v  := 0;  z3v  := 0;  z4v  := 0;  z5v  := 0;
  z6v  := 0;  z7v  := 0;  z8v  := 0;  z9v  := 0;  z10v := 0;
  z11v := 0;  z12v := 0;  z13v := 0;  z14v := 0;  z15v := 0;
  z16v := 0;  z17v := 0;  z18v := 0
|}.

(* Vector addition on weights *)
Definition zvector_plus (v1 v2 : zvector) : zvector := {|
  z1v  := z1v  v1 + z1v  v2;  z2v  := z2v  v1 + z2v  v2;
  z3v  := z3v  v1 + z3v  v2;  z4v  := z4v  v1 + z4v  v2;
  z5v  := z5v  v1 + z5v  v2;  z6v  := z6v  v1 + z6v  v2;
  z7v  := z7v  v1 + z7v  v2;  z8v  := z8v  v1 + z8v  v2;
  z9v  := z9v  v1 + z9v  v2;  z10v := z10v v1 + z10v v2;
  z11v := z11v v1 + z11v v2;  z12v := z12v v1 + z12v v2;
  z13v := z13v v1 + z13v v2;  z14v := z14v v1 + z14v v2;
  z15v := z15v v1 + z15v v2;  z16v := z16v v1 + z16v v2;
  z17v := z17v v1 + z17v v2;  z18v := z18v v1 + z18v v2
|}.

(* Stub semantics: user should refine these *)
Definition clause_sem (subj : noun) (preds : list Zglyph) : zvector :=
  default_zvector.

Definition modulate (emo : emoji) (v : zvector) : zvector :=
  v.

(* The interpreter *)
Fixpoint interp (e : expr) : zvector :=
  match e with
  | EClause subj preds None     => clause_sem subj preds
  | EClause subj preds (Some m) => modulate m (clause_sem subj preds)
  | EDefine _    body           => interp body
  | EInvoke _                  => default_zvector
  | EIf _       then_br        => interp then_br
  | EEval _     _              => default_zvector
  | ECall _     _              => default_zvector
  end.
