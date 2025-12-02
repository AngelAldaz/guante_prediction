from predictor_lsm import PredictorLSM

predictor = PredictorLSM()
letra = predictor.predecir(999, 0, 0, 0, 0, 90.0, False)
print(f"\n\nPrediccion: {letra}")  # ejemplo con posicion_mano=90.0