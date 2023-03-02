
class InfoMessage:
    """Mensaje sobre el entrenamiento."""
    def __init__(self, training_type: str, duration: float, distance: float,
                 speed: float, calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:

        return (f'Tipo de entrenamiento: {self.training_type}; '
                f'Duración: {self.duration:.3f} h; '
                f'Distancia: {self.distance:.3f} km; '
                f'Vel. promedio: {self.speed:.3f} km/h; '
                f'Calorías quemadas: {self.calories:.3f}.')


class Training:
    """Clase de entrenamiento de base."""
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Calcula la distancia recorrida."""

        self.LEN_STEP = 0.65

        distancia_recorrida = self.action * self.LEN_STEP / self.M_IN_KM
        return distancia_recorrida

    def get_mean_speed(self) -> float:
        """Obtiene la velocidad media."""

        velocidad_media = self.get_distance() / self.duration
        return velocidad_media

    def get_spent_calories(self) -> float:
        """Obtiene el número de calorías quemadas."""
        pass

    def name_training_type(self) -> str:
        """Obtiene tipo de entrenamiento"""
        ...

    def show_training_info(self) -> InfoMessage:
        """Devuelve mensaje sobre el entrenamiento completado."""

        mensaje = InfoMessage(self.name_training_type(), self.duration,
                              self.get_distance(), self.get_mean_speed(),
                              self.get_spent_calories())
        return mensaje


class Running(Training):
    """Entrenamiento: correr."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:

        total_calorias_quemadas = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                    * self.get_mean_speed()
                                    + self.CALORIES_MEAN_SPEED_SHIFT)
                                   * self.weight / self.M_IN_KM
                                   * self.duration * 60)
        return total_calorias_quemadas

    def name_training_type(self) -> str:
        return 'Running'


class SportsWalking(Training):
    """Entrenamiento: marcha rápida."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self, action: int,
                 duration: float,
                 weight: float, height) -> None:
        super().__init__(action, duration, weight)

        self.height = height

    def get_spent_calories(self) -> float:
        """Obtiene el número de calorías quemadas durante el entrenamiento."""

        # Fórmula de cálculo de calorías para natación
        total_calorias_quemadas = ((self.CALORIES_WEIGHT_MULTIPLIER
                                    * self.weight
                                    + ((self.get_mean_speed()
                                        * self.KMH_IN_MSEC)**2
                                        / (self.height / self.CM_IN_M))
                                   * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                                   * self.weight)
                                   * self.duration * 60)

        return total_calorias_quemadas

    def name_training_type(self) -> str:
        return 'SportsWalking'


class Swimming(Training):
    """Entrenamiento: natación."""

    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SHIFT = 1.1
    CALORIES_WEIGHT_MULTIPLIER = 2

    def __init__(self, action: int, duration: float,
                 weight: float,
                 length_pool, count_pool) -> None:
        super().__init__(action, duration, weight)
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Obtiene la distancia recorrida durante el entrenamiento."""

        distancia_recorrida = self.action * self.LEN_STEP / self.M_IN_KM
        return distancia_recorrida

    def get_mean_speed(self) -> float:
        """Obtiene la velocidad media."""

        velocidad_media = (
            self.length_pool * self.count_pool
        ) / self.M_IN_KM / self.duration

        return velocidad_media

    def get_spent_calories(self) -> float:
        """Obtiene el número de calorías quemadas durante el entrenamiento."""

        # Fórmula de cálculo de calorías para natación
        total_calorias_quemadas = (
            self.get_mean_speed()
            + self.CALORIES_MEAN_SPEED_SHIFT
        ) * self.CALORIES_WEIGHT_MULTIPLIER * self.weight * self.duration

        return total_calorias_quemadas

    def name_training_type(self) -> str:
        return 'Swimming'


def read_package(workout_type: str, data: list) -> Training:
    """Lee los datos de los sensores."""

    class_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in class_dict:
        training_class = class_dict[workout_type]
        """Comprobamos que los datos contengan la longitud
        de la piscina y el número de piscinas"""
        if workout_type == 'SWM' and len(data) == 5:
            return training_class(data[0], data[1], data[2], data[3], data[4])
        elif workout_type == 'WLK' and len(data) == 4:
            return training_class(data[0], data[1], data[2], data[3])
        else:
            return training_class(data[0], data[1], data[2])


def main(training: Training) -> None:
    """Función principal."""
    info = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
