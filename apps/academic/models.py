from django.db import models
from django.utils import timezone


class Subject(models.Model):
    """Subject/Course Model"""
    subject_code = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text="Unique subject code (e.g., MATH101, ENGL101)"
    )
    subject_name = models.CharField(
        max_length=200,
        db_index=True,
        help_text="Full name of the subject"
    )
    subject_description = models.TextField(
        blank=True,
        null=True,
        help_text="Brief description of the subject"
    )
    units = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=3.0,
        help_text="Number of units"
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the subject is currently active"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subjects'
        verbose_name = 'Subject'
        verbose_name_plural = 'A. Subjects'
        ordering = ['subject_code']
    
    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"


class Syllabus(models.Model):
    """Syllabus Model - Contains overall course structure"""
    subject = models.OneToOneField(
        Subject,
        on_delete=models.CASCADE,
        related_name='syllabus',
        help_text="The subject this syllabus belongs to"
    )
    
    course_description = models.TextField(
        help_text="Detailed course description"
    )
    course_objectives = models.TextField(
        help_text="Learning objectives and outcomes"
    )
    course_outcomes = models.TextField(
        help_text="Expected course outcomes"
    )
    
    grading_system = models.TextField(
        help_text="Grading system and breakdown"
    )
    
    required_textbooks = models.TextField(
        blank=True,
        null=True,
        help_text="Required textbooks and references"
    )
    
    recommended_readings = models.TextField(
        blank=True,
        null=True,
        help_text="Recommended readings and resources"
    )
    
    attendance_policy = models.TextField(
        blank=True,
        null=True,
        help_text="Attendance policy"
    )
    
    grading_policy = models.TextField(
        blank=True,
        null=True,
        help_text="Grading policy and requirements"
    )
    
    classroom_policies = models.TextField(
        blank=True,
        null=True,
        help_text="Classroom policies and expectations"
    )
    
    consultation_hours = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Instructor consultation hours"
    )
    
    instructor_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Name of the instructor"
    )
    
    instructor_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Instructor email address"
    )
    
    instructor_contact = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Instructor contact number"
    )
    
    school_year = models.CharField(
        max_length=20,
        help_text="School year (e.g., 2024-2025)"
    )
    
    semester = models.CharField(
        max_length=20,
        help_text="Semester (e.g., 1st Semester, 2nd Semester)"
    )
    
    is_published = models.BooleanField(
        default=False,
        help_text="Whether the syllabus is published"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'syllabi'
        verbose_name = 'Syllabus'
        verbose_name_plural = 'B.  Syllabus'
        ordering = ['subject__subject_code']
    
    def __str__(self):
        return f"Syllabus for {self.subject.subject_code} - {self.subject.subject_name}"


class Module(models.Model):
    """Module Model - Contains weekly topics and content"""
    
    # Module Types
    class ModuleType(models.TextChoices):
        LECTURE = 'Lecture', 'Lecture'
        LABORATORY = 'Laboratory', 'Laboratory'
        DISCUSSION = 'Discussion', 'Discussion'
        RECITATION = 'Recitation', 'Recitation'
        ASSIGNMENT = 'Assignment', 'Assignment'
        EXAM = 'Exam', 'Exam'
        QUIZ = 'Quiz', 'Quiz'
        PROJECT = 'Project', 'Project'
        ACTIVITY = 'Activity', 'Activity'
        PRESENTATION = 'Presentation', 'Presentation'
    
    syllabus = models.ForeignKey(
        Syllabus,
        on_delete=models.CASCADE,
        related_name='modules',
        help_text="The syllabus this module belongs to"
    )
    
    module_number = models.IntegerField(
        help_text="Module number (e.g., 1, 2, 3...)"
    )
    
    module_title = models.CharField(
        max_length=200,
        help_text="Title of the module"
    )
    
    module_type = models.CharField(
        max_length=20,
        choices=ModuleType.choices,
        default=ModuleType.LECTURE,
        help_text="Type of module"
    )
    
    week_number = models.IntegerField(
        help_text="Week number"
    )
    
    week_title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Title of the week/lesson"
    )
    
    topics = models.TextField(
        help_text="Topics covered in this module"
    )
    
    learning_objectives = models.TextField(
        help_text="Learning objectives for this module"
    )
    
    learning_outcomes = models.TextField(
        help_text="Expected learning outcomes"
    )
    
    activities = models.TextField(
        blank=True,
        null=True,
        help_text="Activities and exercises"
    )
    
    assignments = models.TextField(
        blank=True,
        null=True,
        help_text="Assignments and tasks"
    )

    lessons = models.TextField(
        blank=True,
        null=True,
        help_text="Lessons and Discussions"
    )


    assessments = models.TextField(
        blank=True,
        null=True,
        help_text="Assessment methods"
    )
    
    resources = models.TextField(
        blank=True,
        null=True,
        help_text="Resources and materials needed"
    )
    
    references = models.TextField(
        blank=True,
        null=True,
        help_text="References and readings"
    )
    
    duration = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Duration (e.g., 1 week, 2 weeks)"
    )
    
    start_date = models.DateField(
        blank=True,
        null=True,
        help_text="Start date of the module"
    )
    
    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="End date of the module"
    )
    
    is_completed = models.BooleanField(
        default=False,
        help_text="Whether the module has been completed"
    )
    
    is_published = models.BooleanField(
        default=False,
        help_text="Whether the module is published"
    )
    
    order = models.IntegerField(
        default=0,
        help_text="Order of modules for display"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'modules'
        verbose_name = 'Module'
        verbose_name_plural = 'C. Modules'
        ordering = ['syllabus', 'module_number', 'order']
        unique_together = [['syllabus', 'module_number']]
    
    def __str__(self):
        return f"Module {self.module_number}: {self.module_title}"
    
    @property
    def is_upcoming(self):
        """Check if module is upcoming"""
        if self.start_date:
            return self.start_date > timezone.now().date()
        return False
    
    @property
    def is_current(self):
        """Check if module is currently active"""
        if self.start_date and self.end_date:
            today = timezone.now().date()
            return self.start_date <= today <= self.end_date
        return False
    
    @property
    def is_overdue(self):
        """Check if module is overdue"""
        if self.end_date:
            return self.end_date < timezone.now().date()
        return False
    
    @property
    def module_progress(self):
        """Calculate module progress (simplified)"""
        # This could be expanded based on completed activities
        if self.is_completed:
            return 100
        elif self.is_current:
            return 50
        elif self.is_upcoming:
            return 0
        else:
            return 0

        