(* versare_properties.v *)

Require Import Coq.Init.Nat.
Require Import Coq.Lists.List.
Import ListNotations.
Require Import VersareSyntax.
Require Import VersareSemantics.

(* Determinism: interp can’t produce two different results *)
Theorem interp_deterministic : forall e v1 v2,
  interp e = v1 ->
  interp e = v2 ->
  v1 = v2.
Proof.
  intros. congruence.
Qed.

(* Modulation is a homomorphism over vector addition *)
Theorem modulate_linear : forall m v1 v2,
  modulate m (zvector_plus v1 v2) =
  zvector_plus (modulate m v1) (modulate m v2).
Proof.
  intros. reflexivity.
Qed.
