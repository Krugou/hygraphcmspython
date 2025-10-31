"""
Hygraph CMS Translations Manager
A Streamlit application for managing translations between dev and master environments
"""
import streamlit as st
import os
from dotenv import load_dotenv
from hygraph_client import HygraphClient
from typing import List, Dict, Any
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Hygraph CMS Translations Manager",
    page_icon="🌐",
    layout="wide"
)

# Initialize session state
if 'dev_client' not in st.session_state:
    st.session_state.dev_client = None
if 'master_client' not in st.session_state:
    st.session_state.master_client = None
if 'dev_translations' not in st.session_state:
    st.session_state.dev_translations = []
if 'master_translations' not in st.session_state:
    st.session_state.master_translations = []


def initialize_clients():
    """Initialize Hygraph clients for dev and master environments"""
    dev_endpoint = os.getenv('HYGRAPH_DEV_ENDPOINT')
    master_endpoint = os.getenv('HYGRAPH_MASTER_ENDPOINT')
    dev_token = os.getenv('HYGRAPH_DEV_TOKEN')
    master_token = os.getenv('HYGRAPH_MASTER_TOKEN')
    
    if not all([dev_endpoint, master_endpoint, dev_token, master_token]):
        return False, "Missing environment variables. Please check your .env file."
    
    try:
        st.session_state.dev_client = HygraphClient(dev_endpoint, dev_token)
        st.session_state.master_client = HygraphClient(master_endpoint, master_token)
        return True, "Clients initialized successfully!"
    except Exception as e:
        return False, f"Error initializing clients: {str(e)}"


def fetch_translations(environment: str):
    """Fetch translations from specified environment"""
    try:
        if environment == "dev":
            client = st.session_state.dev_client
            st.session_state.dev_translations = client.get_translations()
            return True, f"Fetched {len(st.session_state.dev_translations)} translations from dev"
        else:
            client = st.session_state.master_client
            st.session_state.master_translations = client.get_translations()
            return True, f"Fetched {len(st.session_state.master_translations)} translations from master"
    except Exception as e:
        return False, f"Error fetching translations: {str(e)}"


def copy_translations_to_master(selected_translations: List[Dict[str, Any]]):
    """Copy selected translations from dev to master"""
    if not st.session_state.master_client:
        return False, "Master client not initialized"
    
    results = {
        "success": 0,
        "failed": 0,
        "errors": []
    }
    
    for translation in selected_translations:
        try:
            # Create translation in master
            created = st.session_state.master_client.create_translation(
                key=translation.get('key'),
                value=translation.get('value'),
                locale=translation.get('locale', 'en')
            )
            
            # Publish the translation
            if created.get('id'):
                st.session_state.master_client.publish_translation(created['id'])
                results["success"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(f"Failed to create: {translation.get('key')}")
        except Exception as e:
            results["failed"] += 1
            results["errors"].append(f"Error with {translation.get('key')}: {str(e)}")
    
    return True, results


# Main UI
st.title("🌐 Hygraph CMS Translations Manager")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    st.subheader("Environment Status")
    
    # Initialize clients button
    if st.button("🔌 Initialize Connections", use_container_width=True):
        success, message = initialize_clients()
        if success:
            st.success(message)
        else:
            st.error(message)
    
    # Show connection status
    if st.session_state.dev_client:
        st.success("✅ Dev environment connected")
    else:
        st.warning("⚠️ Dev environment not connected")
    
    if st.session_state.master_client:
        st.success("✅ Master environment connected")
    else:
        st.warning("⚠️ Master environment not connected")
    
    st.markdown("---")
    
    st.subheader("📖 Quick Guide")
    st.markdown("""
    1. Initialize connections
    2. Fetch translations from dev
    3. Select translations to copy
    4. Copy to master
    5. Verify in master
    """)

# Main content area
col1, col2 = st.columns(2)

with col1:
    st.header("🔧 Development Environment")
    
    if st.button("📥 Fetch Dev Translations", use_container_width=True, type="primary"):
        if not st.session_state.dev_client:
            st.error("Please initialize connections first")
        else:
            with st.spinner("Fetching translations from dev..."):
                success, message = fetch_translations("dev")
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    if st.session_state.dev_translations:
        st.subheader(f"Dev Translations ({len(st.session_state.dev_translations)})")
        
        # Display translations in a table format
        for idx, translation in enumerate(st.session_state.dev_translations):
            with st.expander(f"🔑 {translation.get('key', 'Unknown')} - {translation.get('locale', 'en')}"):
                st.json(translation)
    else:
        st.info("No translations loaded. Click 'Fetch Dev Translations' to load.")

with col2:
    st.header("🚀 Master Environment")
    
    if st.button("📥 Fetch Master Translations", use_container_width=True):
        if not st.session_state.master_client:
            st.error("Please initialize connections first")
        else:
            with st.spinner("Fetching translations from master..."):
                success, message = fetch_translations("master")
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    if st.session_state.master_translations:
        st.subheader(f"Master Translations ({len(st.session_state.master_translations)})")
        
        # Display translations in a table format
        for idx, translation in enumerate(st.session_state.master_translations):
            with st.expander(f"🔑 {translation.get('key', 'Unknown')} - {translation.get('locale', 'en')}"):
                st.json(translation)
    else:
        st.info("No translations loaded. Click 'Fetch Master Translations' to load.")

# Copy section
st.markdown("---")
st.header("📋 Copy Translations from Dev to Master")

if st.session_state.dev_translations:
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("Select Translations to Copy")
        
        # Option to select all
        select_all = st.checkbox("Select All Translations")
        
        selected_indices = []
        
        if select_all:
            selected_indices = list(range(len(st.session_state.dev_translations)))
        else:
            # Individual selection
            for idx, translation in enumerate(st.session_state.dev_translations):
                if st.checkbox(
                    f"{translation.get('key', 'Unknown')} ({translation.get('locale', 'en')})",
                    key=f"select_{idx}"
                ):
                    selected_indices.append(idx)
    
    with col2:
        st.metric("Selected", len(selected_indices))
    
    with col3:
        st.metric("Total", len(st.session_state.dev_translations))
    
    # Copy button
    if selected_indices:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button(
                f"🚀 Copy {len(selected_indices)} Translation(s) to Master",
                use_container_width=True,
                type="primary"
            ):
                if not st.session_state.master_client:
                    st.error("Please initialize connections first")
                else:
                    selected_translations = [
                        st.session_state.dev_translations[idx] 
                        for idx in selected_indices
                    ]
                    
                    with st.spinner("Copying translations to master..."):
                        success, results = copy_translations_to_master(selected_translations)
                        
                        if success:
                            st.success(f"✅ Successfully copied {results['success']} translation(s)")
                            
                            if results['failed'] > 0:
                                st.warning(f"⚠️ Failed to copy {results['failed']} translation(s)")
                                
                                with st.expander("View Errors"):
                                    for error in results['errors']:
                                        st.error(error)
                            
                            # Refresh master translations
                            fetch_translations("master")
else:
    st.info("Load translations from dev environment to enable copying.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Hygraph CMS Translations Manager v1.0</p>
    <p>Make sure to configure your .env file with proper credentials</p>
</div>
""", unsafe_allow_html=True)
