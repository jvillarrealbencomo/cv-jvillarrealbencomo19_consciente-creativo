"""
Profile Preset Service
Version 2025 - Manages profile-specific visibility templates and configurations
"""
from typing import Dict, List, Any


class ProfilePresetService:
    """
    Service to manage profile presets and apply them to models
    """
    
    # Profile definitions
    PROFILES = {
        'qa_analyst': {
            'name': 'QA Analyst',
            'description': 'Quality Assurance Analyst profile focused on manual testing, test planning, and quality processes',
            'default_title': 'QA Analyst',
        },
        'qa_engineer': {
            'name': 'QA Engineer',
            'description': 'QA Engineer profile focused on test automation, CI/CD integration, and technical testing',
            'default_title': 'QA Engineer',
        },
        'data_scientist': {
            'name': 'Data Scientist',
            'description': 'Data Scientist profile focused on machine learning, statistical analysis, and data engineering',
            'default_title': 'Data Scientist',
        }
    }
    
    # Person contact visibility presets
    PERSON_CONTACT_PRESETS = {
        'qa_analyst': {
            'show_email': True,
            'show_phone': True,
            'show_linkedin': True,
            'show_github': False,  # Less emphasis on code
            'show_personal_url': True
        },
        'qa_engineer': {
            'show_email': True,
            'show_phone': True,
            'show_linkedin': True,
            'show_github': True,  # Show technical profiles
            'show_personal_url': True
        },
        'data_scientist': {
            'show_email': True,
            'show_phone': False,  # More professional distance
            'show_linkedin': True,
            'show_github': True,  # Important for data science
            'show_personal_url': True
        }
    }
    
    # WorkExperience content level presets
    EXPERIENCE_PRESETS = {
        'qa_analyst': {
            'default_level': 'summary',  # Medium detail
            'show_responsibilities_summary': True,
            'show_responsibilities_detailed': False,
            'show_achievements': True
        },
        'qa_engineer': {
            'default_level': 'detailed',  # More technical detail
            'show_responsibilities_summary': True,
            'show_responsibilities_detailed': True,
            'show_achievements': True
        },
        'data_scientist': {
            'default_level': 'complete',  # Full detail
            'show_responsibilities_summary': True,
            'show_responsibilities_detailed': True,
            'show_achievements': True
        }
    }
    
    # TechnicalTool subcategory organization presets
    TOOL_SUBCATEGORY_PRESETS = {
        'qa_analyst': {
            'categories': [
                'Operating Systems & Cloud',
                'Quality Engineering & CI/CD',
                'Test Automation',
                'Databases',
                'Programming Languages'
            ],
            'priority_order': [
                'Quality Engineering & CI/CD',
                'Test Automation',
                'Operating Systems & Cloud',
                'Databases',
                'Programming Languages'
            ]
        },
        'qa_engineer': {
            'categories': [
                'Operating Systems & Cloud',
                'Quality Engineering & CI/CD',
                'Test Automation',
                'Databases',
                'Programming Languages'
            ],
            'priority_order': [
                'Test Automation',
                'Quality Engineering & CI/CD',
                'Programming Languages',
                'Operating Systems & Cloud',
                'Databases'
            ]
        },
        'data_scientist': {
            'categories': [
                'Engineering & Big Data',
                'Modeling & Core Programming'
            ],
            'priority_order': [
                'Modeling & Core Programming',
                'Engineering & Big Data'
            ]
        }
    }
    
    # Section visibility presets (which model types to show)
    SECTION_VISIBILITY_PRESETS = {
        'qa_analyst': {
            'work_experience': True,
            'certifications': True,
            'courses': True,
            'education': True,
            'languages': True,
            'technical_tools': True,
            'it_products': False  # Less relevant for analyst role
        },
        'qa_engineer': {
            'work_experience': True,
            'certifications': True,
            'courses': True,
            'education': True,
            'languages': True,
            'technical_tools': True,
            'it_products': True  # Show technical projects
        },
        'data_scientist': {
            'work_experience': True,
            'certifications': True,
            'courses': True,
            'education': True,  # Very important
            'languages': True,
            'technical_tools': True,
            'it_products': True  # Show data projects
        }
    }
    
    @classmethod
    def get_profile_names(cls) -> List[str]:
        """Get list of available profile names"""
        return list(cls.PROFILES.keys())
    
    @classmethod
    def get_profile_info(cls, profile_name: str) -> Dict[str, Any]:
        """Get information about a specific profile"""
        return cls.PROFILES.get(profile_name, {})
    
    @classmethod
    def apply_person_preset(cls, person_model, profile_name: str):
        """
        Apply contact visibility preset to Person model
        
        Args:
            person_model: Person model instance
            profile_name: Profile name (qa_analyst, qa_engineer, data_scientist)
        """
        preset = cls.PERSON_CONTACT_PRESETS.get(profile_name)
        if not preset:
            return
        
        person_model.show_email = preset.get('show_email', True)
        person_model.show_phone = preset.get('show_phone', True)
        person_model.show_linkedin = preset.get('show_linkedin', True)
        person_model.show_github = preset.get('show_github', False)
        person_model.show_personal_url = preset.get('show_personal_url', True)
    
    @classmethod
    def apply_experience_preset(cls, experience_model, profile_name: str):
        """
        Apply content visibility preset to WorkExperience model
        
        Args:
            experience_model: WorkExperience model instance
            profile_name: Profile name
        """
        preset = cls.EXPERIENCE_PRESETS.get(profile_name)
        if not preset:
            return
        
        # Use set_content_level if available, otherwise set flags directly
        if hasattr(experience_model, 'set_content_level'):
            level = preset.get('default_level', 'summary')
            experience_model.set_content_level(level)
        else:
            experience_model.show_responsibilities_summary = preset.get('show_responsibilities_summary', True)
            experience_model.show_responsibilities_detailed = preset.get('show_responsibilities_detailed', False)
            experience_model.show_achievements = preset.get('show_achievements', True)
    
    @classmethod
    def get_tool_categories(cls, profile_name: str) -> List[str]:
        """
        Get valid tool subcategories for a profile
        
        Args:
            profile_name: Profile name
            
        Returns:
            List of category names in priority order
        """
        preset = cls.TOOL_SUBCATEGORY_PRESETS.get(profile_name)
        if not preset:
            return []
        return preset.get('priority_order', preset.get('categories', []))
    
    @classmethod
    def apply_tool_preset(cls, tool_model, profile_name: str, subcategory: str = None, usable: bool = True):
        """
        Apply tool configuration preset
        
        Args:
            tool_model: TechnicalTool model instance
            profile_name: Profile name
            subcategory: Optional subcategory (if None, uses first priority category)
            usable: Whether tool is usable for this profile
        """
        if not subcategory:
            categories = cls.get_tool_categories(profile_name)
            subcategory = categories[0] if categories else None
        
        if hasattr(tool_model, 'set_profile_config'):
            tool_model.set_profile_config(profile_name, usable, subcategory)
    
    @classmethod
    def get_section_visibility(cls, profile_name: str) -> Dict[str, bool]:
        """
        Get which sections should be visible for a profile
        
        Args:
            profile_name: Profile name
            
        Returns:
            Dictionary of section names to visibility flags
        """
        return cls.SECTION_VISIBILITY_PRESETS.get(profile_name, {})
    
    @classmethod
    def apply_model_preset(cls, model_instance, profile_name: str, visible: bool = True):
        """
        Apply generic visibility preset to any model with ProfileVisibilityMixin
        
        Args:
            model_instance: Model instance with ProfileVisibilityMixin
            profile_name: Profile name
            visible: Whether to make visible for this profile
        """
        if hasattr(model_instance, 'set_visibility_for_profile'):
            model_instance.set_visibility_for_profile(profile_name, visible)
    
    @classmethod
    def create_profile_summary(cls, profile_name: str) -> Dict[str, Any]:
        """
        Create a comprehensive summary of profile settings
        
        Args:
            profile_name: Profile name
            
        Returns:
            Dictionary with all profile settings
        """
        return {
            'profile_info': cls.get_profile_info(profile_name),
            'person_contacts': cls.PERSON_CONTACT_PRESETS.get(profile_name, {}),
            'experience_defaults': cls.EXPERIENCE_PRESETS.get(profile_name, {}),
            'tool_categories': cls.get_tool_categories(profile_name),
            'section_visibility': cls.get_section_visibility(profile_name)
        }
    
    @classmethod
    def apply_full_preset(cls, db_session, profile_name: str):
        """
        Apply preset to all existing records in database
        
        Args:
            db_session: SQLAlchemy session
            profile_name: Profile name to apply
            
        Note: This is a bulk operation that should be used carefully
        """
        from app.models import (
            Person, WorkExperience, TechnicalTool, 
            Education, Certification, Course, Language, ITProduct
        )
        
        section_visibility = cls.get_section_visibility(profile_name)
        
        # Apply to Person records
        for person in db_session.query(Person).all():
            cls.apply_person_preset(person, profile_name)
        
        # Apply to WorkExperience records
        for exp in db_session.query(WorkExperience).all():
            cls.apply_experience_preset(exp, profile_name)
            cls.apply_model_preset(exp, profile_name, section_visibility.get('work_experience', True))
        
        # Apply to TechnicalTool records
        for tool in db_session.query(TechnicalTool).all():
            cls.apply_tool_preset(tool, profile_name)
            cls.apply_model_preset(tool, profile_name, section_visibility.get('technical_tools', True))
        
        # Apply generic visibility to other models
        model_section_map = [
            (Education, 'education'),
            (Certification, 'certifications'),
            (Course, 'courses'),
            (Language, 'languages'),
            (ITProduct, 'it_products')
        ]
        
        for model_class, section_name in model_section_map:
            visible = section_visibility.get(section_name, True)
            for instance in db_session.query(model_class).all():
                cls.apply_model_preset(instance, profile_name, visible)
        
        db_session.commit()
