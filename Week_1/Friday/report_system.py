"""Test-report system: TestResult, Suite, Reporter (+ subclasses).

Fill in every TODO. Run `python3 check_exercise.py N` after each part.
Until a method is finished it raises NotImplementedError; that is normal.
"""


class TestResult:
    """One test outcome. Validated, with two alternative constructors."""

    # Class variables (shared by every TestResult). Given to you.
    VALID_STATUSES = ("PASS", "FAIL", "SKIPPED", "ERROR")
    total_created = 0

    def __init__(self, test_id, status, duration=0.0, message=""):
        # TODO 1.1: validate test_id with TestResult.is_valid_id (ValueError if bad)
        #           and store it in self._test_id
        
        if not TestResult.is_valid_id(test_id):
            raise ValueError(f"Invalid test ID: {test_id}")
        
        self._test_id = test_id
        
        # TODO 1.2: set self.status and self.duration THROUGH the properties below,
        #           so validation runs. Store message as a plain attribute.

        self.status = status
        self.duration = duration

        self.message = message

        # TODO 1.3: increase TestResult.total_created ONLY after everything above
        #           succeeded (an object that fails validation must not be counted)
        
        TestResult.total_created += 1

    # ---- static helper ----------------------------------------------------
    @staticmethod
    def is_valid_id(test_id):
        """True for text like 'TC-001': 'TC-' followed by one or more digits."""
        # TODO 1.4: return True/False. Never raise, even for None or numbers.
        if not isinstance(test_id, str):
            return False

        if not test_id.startswith("TC-"):
            return False

        return test_id[3:].isdigit()

    # ---- encapsulated attributes -------------------------------------------
    @property
    def test_id(self):
        # TODO 1.5: return the stored id. Read-only: do NOT write a setter.
        return self._test_id

    @property
    def status(self):
        # TODO 1.6: return the stored status
        return self._status

    @status.setter
    def status(self, value):
        # TODO 1.6: must be text; strip and upper-case it; it must be in
        #           VALID_STATUSES, otherwise raise ValueError (include the bad
        #           value in the message). Only then store it in self._status.
        if not isinstance(value, str):
            raise ValueError(f"Invalid status: {value}")

        normalized = value.strip().upper()

        if normalized not in TestResult.VALID_STATUSES:
            raise ValueError(f"Invalid status: {value}")

        self._status = normalized

    @property
    def duration(self):
        # TODO 1.7: return the stored duration
        return self._duration

    @duration.setter
    def duration(self, value):
        # TODO 1.7: not int/float (or a bool) -> TypeError; negative -> ValueError;
        #           otherwise store float(value) in self._duration
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"Invalid duration type: {value}")

        if value < 0:
            raise ValueError(f"Duration cannot be negative: {value}")

        self._duration = float(value)

    @property
    def is_passed(self):
        # TODO 1.8: True only when the status is "PASS". Read-only.
        return self.status == "PASS"

    # ---- class methods ------------------------------------------------------
    @classmethod
    def how_many(cls):
        # TODO 1.9: return the class-level counter
        return cls.total_created 

    @classmethod
    def from_dict(cls, data):
        # TODO 1.10: keys "test_id" and "status" are required (ValueError naming the
        #            missing key); "duration" (default 0.0) and "message"
        #            (default "") are optional. Build the object with cls(...),
        #            NOT TestResult(...).
        
        if "test_id" not in data:
            raise ValueError("Missing Required Key: test_id")

        if "status" not in data:
            raise ValueError("Missing required key: status")

        return cls(data["test_id"], data["status"], data.get("duration", 0.0), data.get("message", ""))

    @classmethod
    def from_csv_line(cls, line):
        # TODO 1.11: "TC-001,PASS,1.2,Timeout after 30s" -> TestResult.
        #            Only the first two fields are required. The message may
        #            itself contain commas (hint: split with a limit).
        #            Strip spaces around each field. Too few fields -> ValueError.
        
        parts = [part.strip() for part in line.split(",", 3)]

        if len(parts) < 2:
            raise ValueError("CSV line requires test_id and status")

        test_id = parts[0]
        status = parts[1]
        duration = float(parts[2]) if len(parts) > 2 and parts[2] else 0.0
        message = parts[3] if len(parts) > 3 else ""


        return cls(test_id, status, duration, message)

    # ---- text forms ----------------------------------------------------------
    def __str__(self):
        # TODO 1.12: "TC-001 PASS 1.2s"  (add " - <message>" only if there is one)
        
        txt = f"{self.test_id} {self.status} {self.duration}s"

        if self.message:
            txt += f" - {self.message}"

        return txt

    def __repr__(self):
        # TODO 1.12: "TestResult('TC-001', 'PASS', 1.2)"; use the REAL class name
        #            via type(self).__name__ so subclasses print correctly
        return f"{type(self).__name__}('{self.test_id}', '{self.status}', {self.duration})"


class Suite:
    """A named collection of TestResult objects (has-a, not is-a list)."""

    def __init__(self, name):
        # TODO 2.1: name must be non-empty text after strip() (else ValueError);
        #           store the stripped name in self.name

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Suite Name must be non-empty text")

        # TODO 2.2: create the per-object list self._results here (NOT in the class body)
        self.name = name.strip()
        self._results = []

    @classmethod
    def from_rows(cls, name, rows):
        # TODO 2.3: build a suite and add TestResult.from_dict(row) for every row
        suite = cls(name)

        for row in rows:
            result = TestResult.from_dict(row)
            suite.add(result)

        return suite

    def add(self, result):
        # TODO 2.4: not a TestResult -> TypeError; a test_id already in the suite
        #           -> ValueError (mention the id); otherwise append
        
        if not isinstance(result, TestResult):
            raise TypeError(f"Result must be a TestResult object")

        for existing in self._results:
            if existing.test_id == result.test_id:
                raise ValueError(f"Duplicate test ID: {result.test_id}")

        self._results.append(result)

    @property
    def results(self):
        # TODO 2.5: return a COPY of the internal list
        return self._results.copy()

    def count(self):
        # TODO 2.5: number of results
        return len(self._results)

    @property
    def pass_rate(self):
        # TODO 2.6: percent (0-100) of results whose status is PASS, out of ALL
        #           results (SKIPPED counts in the total). Empty suite -> 0.0
        
        if self.count() == 0:
            return 0.0

        passed = sum(1 for result in self._results if result.is_passed)

        return (passed / self.count()) * 100

    @property
    def total_duration(self):
        # TODO 2.7: sum of all durations
        
        return sum(result.duration for result in self._results)

    def counts_by_status(self):
        # TODO 2.7: dict with EVERY valid status as a key, e.g.
        #           {"PASS": 2, "FAIL": 1, "SKIPPED": 1, "ERROR": 0}
        
        counts = {status: 0 for status in TestResult.VALID_STATUSES}

        for result in self._results:
            counts[result.status] += 1

        return counts

    def failures(self):
        # TODO 2.8: list of results whose status is FAIL or ERROR (suite order)
        
        failedResults = []

        for result in self._results:
            if result.status == "FAIL" or result.status == "ERROR":
                failedResults.append(result)

        return failedResults

    def slowest(self, n=1):
        # TODO 2.8: the n slowest results, slowest first (sorted with a key)
        
        sorted_result = sorted(self._results, key=lambda result: result.duration, reverse=True)

        return sorted_result[:n]


class Reporter:
    """Base class: presentation only. Subclasses override render()."""

    def __init__(self, suite):
        # TODO 3.1: suite must be a Suite (else TypeError); store it as self.suite
        
        if not isinstance(suite, Suite):
            raise TypeError("Suite must be a Suite object.")

        self.suite = suite

    @staticmethod
    def pad(text, width):
        # TODO 3.2: str(text) left-justified in `width` characters. Never cut text.
        return str(text).ljust(width)

    @staticmethod
    def format_percent(value):
        # TODO 3.2: 66.666 -> "66.7%"
        return f"{value:.1f}%"

    def render(self):
        # TODO 3.3: the base class has no format: raise NotImplementedError with a
        #           helpful message naming the class (type(self).__name__)
        raise NotImplementedError(f"{type(self).__name__} must implement render")

    def line_count(self):
        # TODO 3.4: number of lines in self.render(). Write it ONCE here;
        #           subclasses inherit it.
        return len(self.render().splitlines())


class TextReporter(Reporter):
    def render(self):
        # TODO 3.5: see README for the exact layout (header, one row per result,
        #           "Pass rate: 50.0%"). Use self.pad and self.format_percent.
        
        lines = [f"=== {self.suite.name} ==="]

        for result in self.suite.results:
            test_id = self.pad(result.test_id, 8)
            status = self.pad(result.status, 9)
            duration = f"{result.duration:>5.1f}s"
            
            lines.append(f"{test_id}{status}{duration}")
        
        lines.append(f"Pass rate: {self.format_percent(self.suite.pass_rate)}")

        return "\n".join(lines)


class CsvReporter(Reporter):
    HEADER = "test_id,status,duration,message"

    @staticmethod
    def clean_cell(text):
        # TODO 3.6: commas -> ";" and newlines -> " " so one cell stays one cell
        
        cleaned = str(text).replace(",", ";")
        cleaned = cleaned.replace("\n", " ")

        return cleaned
    
    def render(self):
        # TODO 3.6: see README for the exact layout
        
        lines = [self.HEADER]

        for result in self.suite.results:
            line = f"{result.test_id}," f"{result.status}," f"{result.duration:.1f}," f"{self.clean_cell(result.message)}"

            lines.append(line)

        return "\n".join(lines)

# STRETCH 1: add class MarkdownReporter(Reporter) here (see README).
