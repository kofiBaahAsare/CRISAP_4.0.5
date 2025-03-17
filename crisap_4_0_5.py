##!/usr/bin/env python3
# 🚀 CRISAP 4.0.5 - AI-Powered Climate Risk Intelligence System
# Integrated with Auto-Setup and Self-Healing Capabilities

import os
import sys
import subprocess
import platform
import shutil
import logging
import time
import traceback
import json
import hashlib
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Union, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "crisap.log"
        ))
    ]
)
logger = logging.getLogger("CRISAP")

# Constants
APP_VERSION = "4.0.5"
APP_TITLE = f"🚀 CRISAP {APP_VERSION} - AI-Powered Climate Risk Intelligence System"
REQUIRED_PYTHON_VERSION = (3, 7)
SETUP_TIMESTAMP = time.strftime("%Y%m%d_%H%M%S")

# Console colors for better readability
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def color_print(text: str, color: str) -> None:
    """Print colored text if terminal supports it."""
    if sys.stdout.isatty():  # Only use colors when outputting to terminal
        print(f"{color}{text}{Colors.ENDC}")
    else:
        print(text)

def print_banner() -> None:
    """Print the CRISAP banner."""
    banner = f"""
    {Colors.BLUE}{Colors.BOLD}╔═══════════════════════════════════════════════════════════╗{Colors.ENDC}
    {Colors.BLUE}{Colors.BOLD}║                      CRISAP {APP_VERSION}                         ║{Colors.ENDC}
    {Colors.BLUE}{Colors.BOLD}║     AI-Powered Climate Risk Intelligence System           ║{Colors.ENDC}
    {Colors.BLUE}{Colors.BOLD}╚═══════════════════════════════════════════════════════════╝{Colors.ENDC}
    """
    print(banner)

# 🔧 Self-Healing System Functions

class SystemHealth:
    """System health monitoring and self-healing functionality."""
    
    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.health_check_results = {}
        
    def run_self_diagnostics(self) -> Dict[str, bool]:
        """Run a comprehensive system diagnostics."""
        logger.info("Running self-diagnostics...")
        
        # Check Python version
        python_version_ok = self._check_python_version()
        
        # Check directory structure
        directories_ok = self._check_directories()
        
        # Check dependencies
        dependencies_ok = self._check_dependencies()
        
        # Check API keys
        api_keys_ok = self._check_api_keys()
        
        # Check disk space
        disk_space_ok = self._check_disk_space()
        
        # Store results
        self.health_check_results = {
            "python_version": python_version_ok,
            "directories": directories_ok,
            "dependencies": dependencies_ok,
            "api_keys": api_keys_ok,
            "disk_space": disk_space_ok,
            "overall": all([python_version_ok, directories_ok, dependencies_ok, api_keys_ok, disk_space_ok])
        }
        
        return self.health_check_results
    
    def _check_python_version(self) -> bool:
        """Check if the current Python version meets requirements."""
        current_version = sys.version_info
        meets_requirement = current_version >= REQUIRED_PYTHON_VERSION
        
        if meets_requirement:
            logger.info(f"✓ Python version {current_version.major}.{current_version.minor}.{current_version.micro} detected (meets requirements)")
        else:
            logger.warning(f"✗ Python version {current_version.major}.{current_version.minor}.{current_version.micro} detected")
            logger.warning(f"  Required: Python {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]} or higher")
            
        return meets_requirement
    
    def _check_directories(self) -> bool:
        """Check if required directories exist and are writable."""
        required_dirs = [
            "config", "data", "logs", "models", "exports", "cache", "temp"
        ]
        
        all_ok = True
        for dir_name in required_dirs:
            dir_path = os.path.join(self.base_path, dir_name)
            
            # Check if directory exists, create if not
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path, exist_ok=True)
                    logger.info(f"✓ Created missing directory: {dir_path}")
                except Exception as e:
                    logger.error(f"✗ Failed to create directory {dir_path}: {str(e)}")
                    all_ok = False
                    continue
            
            # Check if directory is writable
            if not os.access(dir_path, os.W_OK):
                logger.error(f"✗ Directory not writable: {dir_path}")
                all_ok = False
        
        return all_ok
    
    def _check_dependencies(self) -> bool:
        """Check if all required dependencies are installed."""
        required_packages = [
            "numpy", "pandas", "streamlit", "openai", "supabase", "folium", "web3"
        ]
        
        all_ok = True
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
                all_ok = False
        
        if missing_packages:
            logger.warning(f"Missing dependencies: {', '.join(missing_packages)}")
            logger.info("Attempting to install missing dependencies...")
            
            for package in missing_packages:
                try:
                    logger.info(f"Installing {package}...")
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", package],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    logger.info(f"✓ Successfully installed {package}")
                except subprocess.CalledProcessError:
                    logger.error(f"✗ Failed to install {package}")
                    all_ok = False
        
        return all_ok
    
    def _check_api_keys(self) -> bool:
        """Check if required API keys are available."""
        required_keys = [
            "OPENAI_API_KEY", "SUPABASE_URL", "SUPABASE_KEY", "INFURA_PROJECT_ID"
        ]
        
        all_ok = True
        missing_keys = []
        
        # Check environment variables
        for key in required_keys:
            if not os.environ.get(key):
                missing_keys.append(key)
        
        # If any keys are missing, check .env file
        if missing_keys:
            env_path = os.path.join(self.base_path, ".env")
            if os.path.exists(env_path):
                logger.info("Found .env file, checking for missing keys...")
                
                # Read .env file
                with open(env_path, "r") as f:
                    env_content = f.read()
                
                # Check if each missing key is in the .env file
                for key in missing_keys[:]:
                    if f"{key}=" in env_content:
                        missing_keys.remove(key)
            
            # If keys are still missing, create template .env file
            if missing_keys:
                logger.warning(f"Missing API keys: {', '.join(missing_keys)}")
                if not os.path.exists(env_path):
                    self._create_env_template(env_path)
                all_ok = False
        
        return all_ok
    
    def _check_disk_space(self) -> bool:
        """Check if there's enough disk space."""
        min_space_mb = 500  # Minimum 500 MB required
        
        try:
            if platform.system() == "Windows":
                free_space = shutil.disk_usage(self.base_path).free
            else:
                stat = os.statvfs(self.base_path)
                free_space = stat.f_frsize * stat.f_bavail
            
            free_space_mb = free_space / (1024 * 1024)
            
            if free_space_mb < min_space_mb:
                logger.warning(f"Low disk space: {free_space_mb:.2f} MB available, minimum {min_space_mb} MB required")
                return False
            else:
                logger.info(f"✓ Sufficient disk space: {free_space_mb:.2f} MB available")
                return True
        except Exception as e:
            logger.error(f"✗ Failed to check disk space: {str(e)}")
            return False
    
    def _create_env_template(self, env_path: str) -> None:
        """Create a template .env file."""
        template = f"""# CRISAP Environment Variables
# Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
INFURA_PROJECT_ID=your_infura_project_id_here

# Application Settings
LOG_LEVEL=INFO
DEPLOYMENT_ENV=development
ENABLE_BLOCKCHAIN=false
ENABLE_ADVANCED_ANALYTICS=true
ENABLE_REPORT_GENERATION=true

# Data Storage
DATA_STORAGE_PATH={os.path.join(self.base_path, "data")}
MODELS_PATH={os.path.join(self.base_path, "models")}
EXPORTS_PATH={os.path.join(self.base_path, "exports")}
CACHE_PATH={os.path.join(self.base_path, "cache")}
TEMP_PATH={os.path.join(self.base_path, "temp")}

# Security
JWT_SECRET=change_this_to_a_random_string
"""
        
        try:
            with open(env_path, "w") as f:
                f.write(template)
            logger.info(f"✓ Created template .env file at {env_path}")
        except Exception as e:
            logger.error(f"✗ Failed to create .env file: {str(e)}")
    
    def perform_self_healing(self) -> bool:
        """Attempt to fix any issues found during diagnostics."""
        logger.info("Performing self-healing...")
        
        # Run diagnostics if not already run
        if not self.health_check_results:
            self.run_self_diagnostics()
        
        # Fix issues based on diagnostics results
        fixed_issues = []
        failed_fixes = []
        
        # 1. Fix missing directories
        if not self.health_check_results.get("directories", True):
            logger.info("Fixing directory structure...")
            dirs_fixed = self._fix_directories()
            if dirs_fixed:
                fixed_issues.append("directories")
            else:
                failed_fixes.append("directories")
        
        # 2. Fix missing dependencies
        if not self.health_check_results.get("dependencies", True):
            logger.info("Fixing dependencies...")
            deps_fixed = self._fix_dependencies()
            if deps_fixed:
                fixed_issues.append("dependencies")
            else:
                failed_fixes.append("dependencies")
        
        # Log results
        if fixed_issues:
            logger.info(f"✓ Self-healing fixed: {', '.join(fixed_issues)}")
        if failed_fixes:
            logger.warning(f"✗ Self-healing failed to fix: {', '.join(failed_fixes)}")
        
        # Return True if all issues were fixed
        return len(failed_fixes) == 0
    
    def _fix_directories(self) -> bool:
        """Fix directory structure issues."""
        required_dirs = [
            "config", "data", "logs", "models", "exports", "cache", "temp"
        ]
        
        all_fixed = True
        for dir_name in required_dirs:
            dir_path = os.path.join(self.base_path, dir_name)
            
            # Create directory if it doesn't exist
            if not os.path.exists(dir_path):
                try:
                    os.makedirs(dir_path, exist_ok=True)
                    logger.info(f"✓ Created directory: {dir_path}")
                except Exception as e:
                    logger.error(f"✗ Failed to create directory {dir_path}: {str(e)}")
                    all_fixed = False
            
            # Fix permissions if directory is not writable
            elif not os.access(dir_path, os.W_OK):
                try:
                    if platform.system() != "Windows":
                        os.chmod(dir_path, 0o755)  # rwxr-xr-x
                        logger.info(f"✓ Fixed permissions for directory: {dir_path}")
                    else:
                        logger.warning(f"Cannot fix permissions on Windows for: {dir_path}")
                        all_fixed = False
                except Exception as e:
                    logger.error(f"✗ Failed to fix permissions for {dir_path}: {str(e)}")
                    all_fixed = False
        
        return all_fixed
    
    def _fix_dependencies(self) -> bool:
        """Fix dependency issues."""
        required_packages = [
            "numpy", "pandas", "scipy", "scikit-learn", "xgboost", "joblib",
            "tensorflow", "torch", "transformers", "geopandas",
            "shapely", "rasterio", "fiona", "pyproj", "folium", "h3", "requests",
            "beautifulsoup4", "matplotlib", "seaborn", "plotly", "dash", "streamlit",
            "streamlit_folium", "reportlab", "python-docx", "xlsxwriter", "boto3",
            "azure-storage-blob", "google-cloud-storage", "web3", "supabase-py",
            "pyjwt", "openai", "nltk", "spacy", "langchain", "pycountry", "python-dotenv"
        ]
        
        # Optional: Try to install climada, but don't fail if it doesn't work
        try:
            __import__("climada")
        except ImportError:
            try:
                logger.info("Installing climada...")
                subprocess