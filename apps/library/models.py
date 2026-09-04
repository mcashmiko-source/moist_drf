from django.db import models
from django.utils import timezone

class LibraryCatalog(models.Model):
    # Primary identifiers
    id = models.AutoField(primary_key=True)
    control_no = models.CharField(max_length=50, unique=True, db_index=True, 
                                   help_text="Control number for the record")
    date_time_stamp = models.DateTimeField(default=timezone.now, 
                                           help_text="Date and time of record creation/update")
    fixed_length_data = models.CharField(max_length=100, blank=True, null=True,
                                         help_text="Fixed length data")
    
    # ISBN/ISSN/Price
    isbn = models.CharField(max_length=20, blank=True, null=True, 
                            help_text="International Standard Book Number")
    issn = models.CharField(max_length=20, blank=True, null=True,
                            help_text="International Standard Serial Number")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Cataloging Source
    cataloging_source_a = models.CharField(max_length=100, blank=True, null=True,
                                           help_text="Cataloging source agency")
    cataloging_source_b = models.CharField(max_length=100, blank=True, null=True,
                                           help_text="Language of cataloging")
    cataloging_source_e = models.CharField(max_length=100, blank=True, null=True,
                                           help_text="Description conventions")
    
    # Author and Title
    main_author = models.CharField(max_length=200, db_index=True,
                                   help_text="Main author of the work")
    title_statement = models.TextField(help_text="Title statement")
    title_author = models.CharField(max_length=200, blank=True, null=True,
                                    help_text="Title author/statement of responsibility")
    
    # Edition and Publication
    edition = models.CharField(max_length=100, blank=True, null=True,
                               help_text="Edition statement")
    publication_place = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    publication_year = models.CharField(max_length=20, blank=True, null=True,
                                        help_text="Year of publication")
    
    # Physical Description
    pages = models.CharField(max_length=100, blank=True, null=True,
                             help_text="Number of pages")
    illustrations = models.CharField(max_length=100, blank=True, null=True,
                                     help_text="Illustrations note")
    size = models.CharField(max_length=50, blank=True, null=True,
                            help_text="Physical dimensions")
    volume = models.CharField(max_length=50, blank=True, null=True,
                              help_text="Volume number")
    
    # Content, Media, Carrier Types (MARC 21)
    content_type = models.CharField(max_length=50, blank=True, null=True,
                                    help_text="Content type term")
    content_code = models.CharField(max_length=10, blank=True, null=True,
                                    help_text="Content type code")
    media_type = models.CharField(max_length=50, blank=True, null=True,
                                  help_text="Media type term")
    media_code = models.CharField(max_length=10, blank=True, null=True,
                                  help_text="Media type code")
    carrier_type = models.CharField(max_length=50, blank=True, null=True,
                                    help_text="Carrier type term")
    carrier_code = models.CharField(max_length=10, blank=True, null=True,
                                    help_text="Carrier type code")
    
    # Series and Notes
    series_title = models.CharField(max_length=200, blank=True, null=True,
                                    help_text="Series title")
    general_note = models.TextField(blank=True, null=True,
                                    help_text="General notes")
    bibliography_note = models.TextField(blank=True, null=True,
                                         help_text="Bibliography note")
    
    # Source Information
    source_vendor = models.CharField(max_length=200, blank=True, null=True)
    source_date = models.DateField(blank=True, null=True)
    
    # Subjects (MARC 21)
    subject_topic = models.CharField(max_length=200, blank=True, null=True,
                                     help_text="Subject topic")
    subject_form = models.CharField(max_length=200, blank=True, null=True,
                                    help_text="Subject form")
    genre = models.CharField(max_length=200, blank=True, null=True,
                             help_text="Genre/Form")
    
    # Library Location
    library_name = models.CharField(max_length=200, db_index=True,
                                    help_text="Library name")
    section = models.CharField(max_length=100, blank=True, null=True,
                               help_text="Library section/collection")
    call_number = models.CharField(max_length=100, db_index=True,
                                   help_text="Call number")
    
    # Accession and Identifiers
    accession_no = models.CharField(max_length=50, blank=True, null=True,
                                    help_text="Accession number")
    barcode = models.CharField(max_length=50, blank=True, null=True,
                               help_text="Barcode")
    rfid = models.CharField(max_length=50, blank=True, null=True,
                            help_text="RFID tag")
    
    # Availability and Usage
    availability = models.BooleanField(default=True,
                                       help_text="Is item available")
    year = models.CharField(max_length=20, blank=True, null=True,
                            help_text="Year of acquisition/coverage")
    course = models.CharField(max_length=200, blank=True, null=True,
                              help_text="Associated course")
    
    # Cover Image (URL or file path)
    cover_image = models.URLField(max_length=500, blank=True, null=True,
                                  help_text="URL to cover image")
    
    # Added Entry Elements (MARC 21 7XX)
    added_entry_elements = models.TextField(blank=True, null=True,
                                            help_text="Added entry elements")
    corporate_name = models.CharField(max_length=200, blank=True, null=True,
                                      help_text="Corporate name added entry")
    personal_name = models.CharField(max_length=200, blank=True, null=True,
                                     help_text="Personal name added entry")
    
    # Faceted Subject Access
    faceted_topical_terms = models.TextField(blank=True, null=True,
                                             help_text="Faceted topical terms")
    genre_form = models.CharField(max_length=200, blank=True, null=True,
                                  help_text="Genre form")
    topical_term = models.CharField(max_length=200, blank=True, null=True,
                                    help_text="Topical term")
    geographical_name = models.CharField(max_length=200, blank=True, null=True,
                                         help_text="Geographical name")
    uniform_title = models.CharField(max_length=200, blank=True, null=True,
                                     help_text="Uniform title")
    chronological_term = models.CharField(max_length=200, blank=True, null=True,
                                          help_text="Chronological term")
    
    # Subject Corporate/Personal Names
    subject_corporate_name = models.CharField(max_length=200, blank=True, null=True,
                                              help_text="Subject corporate name")
    subject_personal_name = models.CharField(max_length=200, blank=True, null=True,
                                             help_text="Subject personal name")
    
    # Summary/Abstract
    summary = models.TextField(blank=True, null=True,
                               help_text="Summary or abstract")
    
    # Additional fields from your CSV
    publication_distribution = models.CharField(max_length=200, blank=True, null=True,
                                                help_text="Publication distribution")
    main_corporate_name = models.CharField(max_length=200, blank=True, null=True,
                                           help_text="Main corporate name")
    ddc_number = models.CharField(max_length=50, blank=True, null=True,
                                  help_text="Dewey Decimal Classification number")
    leader = models.CharField(max_length=50, blank=True, null=True,
                              help_text="MARC leader")
    control_number_identifier = models.CharField(max_length=50, blank=True, null=True,
                                                 help_text="Control number identifier")
    acquisition_type_id = models.CharField(max_length=50, blank=True, null=True,
                                           help_text="Acquisition type ID")
    acquisition_custom = models.CharField(max_length=200, blank=True, null=True,
                                          help_text="Acquisition custom")
    programs = models.CharField(max_length=200, blank=True, null=True,
                                help_text="Programs")
    archived_at = models.DateTimeField(blank=True, null=True,
                                       help_text="Archived at")
    deleted_at = models.DateTimeField(blank=True, null=True,
                                      help_text="Deleted at")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'library_catalog'
        verbose_name = 'Library Catalog'
        verbose_name_plural = 'Book Holdings'
        indexes = [
            models.Index(fields=['control_no']),
            models.Index(fields=['isbn']),
            models.Index(fields=['issn']),
            models.Index(fields=['main_author']),
            models.Index(fields=['call_number']),
            models.Index(fields=['library_name']),
            models.Index(fields=['availability']),
        ]
        # unique_together = ['main_author','title_statement']
        ordering = ['-date_time_stamp']
    
    def __str__(self):
        return f"{self.control_no} - {self.title_statement[:50]}"