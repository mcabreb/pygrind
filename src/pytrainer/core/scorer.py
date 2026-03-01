"""Score calculator for competition exercises."""

BASE_POINTS: dict[int, int] = {1: 10, 2: 20, 3: 35, 4: 50, 5: 75}


class Scorer:
    """Calculates points for a solved problem."""

    @staticmethod
    def calculate(
        tier: int,
        time_spent: float,
        time_estimate: int,
        attempts: int,
        solution_viewed: bool,
    ) -> int:
        """Calculate score for a problem.

        Args:
            tier: Exercise difficulty tier (1-5).
            time_spent: Seconds spent on the problem.
            time_estimate: Estimated time in minutes from exercise metadata.
            attempts: Number of wrong attempts before correct submission.
            solution_viewed: Whether the user viewed the solution.

        Returns:
            Integer score (truncated, not rounded).
        """
        if solution_viewed:
            return 0

        base = BASE_POINTS[tier]

        # Time bonus: +10% if solved in less than half the estimate
        threshold = (time_estimate * 60) / 2
        if time_spent < threshold:
            base = int(base * 1.1)

        # Wrong attempt penalty: -10% per attempt, max -50%
        penalty = min(attempts * 0.10, 0.50)
        return int(base * (1 - penalty))
