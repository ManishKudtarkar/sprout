class RemedyRecommender:
    def get_remedies_for_condition(self, condition_data, user_profile=None):
        """
        Extracts and formats remedies for a given condition, filtering by user profile.
        """
        remedies = condition_data.get("remedies", [])
        if not remedies:
            return ["No specific natural remedies found for this condition."]
        
        if user_profile:
            remedies = self._personalize_remedies(remedies, user_profile)
            
        return remedies

    def _personalize_remedies(self, remedies, profile):
        body_type = profile.get("body_type", "neutral").lower()
        age = profile.get("age")
        
        try:
            age = int(age)
        except (ValueError, TypeError):
            age = 25 # Default to adult if unknown

        filtered_remedies = []
        
        for remedy in remedies:
            remedy_lower = remedy.lower()
            warning = None
            is_unsafe = False
            
            # 1. AGE-BASED FILTERING (Pediatric/Geriatric Safety)
            if age < 12: # Child
                if any(x in remedy_lower for x in ["aspirin", "intense exercise", "steam inhalation", "essential oil"]):
                    warning = " (Consult Pediatrician first)"
                if "honey" in remedy_lower and age < 1:
                    is_unsafe = True # Botulism risk for infants
            
            elif age > 65: # Senior
                if any(x in remedy_lower for x in ["strenuous", "heavy lifting", "nsaids"]):
                    warning = " (Use caution or consult doctor)"

            # 2. BODY TYPE (Ayurvedic/Constitution)
            # Heat Body Rules (Avoid heating elements)
            if body_type == "heat":
                if any(x in remedy_lower for x in ["ginger", "pepper", "spicy", "hot", "garlic", "sauna"]):
                    warning = " (Caution: May increase body heat)"
            
            # Cold Body Rules (Avoid cooling elements)
            if body_type == "cold":
                if any(x in remedy_lower for x in ["cold", "mint", "cucumber", "ice", "raw salad"]):
                    warning = " (Caution: May be too cooling)"

            if not is_unsafe:
                if warning:
                    filtered_remedies.append(remedy + warning)
                else:
                    filtered_remedies.append(remedy)
                
        return filtered_remedies

    def explain_remedy(self, remedy_name):
        """
        Placeholder for future logic to explain why a remedy works.
        """
        # In a real system, this would query a knowledge base of mechanism of action.
        explanations = {
            "Ginger tea": "Ginger has anti-inflammatory properties and helps soothe the throat.",
            "Honey and lemon": "Honey coats the throat and lemon provides Vitamin C.",
            "Steam inhalation": "Helps clear nasal congestion.",
            "Rest": "Allows the body to focus energy on fighting the infection.",
            "Hydration": "Essential for bodily functions and recovery.",
            "Hydration with electrolytes": "Replenishes essential minerals lost due to dehydration.",
            "Brat diet": "Bland foods (Banana, Rice, Apple, Toast) that are easy on the stomach.",
            "Probiotics": "Restores healthy gut bacteria to aid digestion.",
            "Aloe vera gel": "Soothes inflammation and provides a cooling effect for skin.",
            "Cool bath": "Helps lower body temperature and soothe skin irritation.",
            "Lean forward (do NOT tilt head back)": "Prevents blood from flowing down the throat.",
            "Pinch the soft part of the nose": "Applies pressure to stop bleeding vessels.",
            "Ice pack": "Constricts blood vessels to reduce swelling or bleeding.",
            "Look at the horizon": "Helps reorient the brain's balance system.",
            "Ginger": "Natural anti-nauseant that soothes the stomach.",
            "Cold compress": "Reduces swelling and numbs pain.",
            "Coffee": "Caffeine can constrict blood vessels to relieve headache."
        }
        # Check for partial matches if exact match fails
        if remedy_name in explanations:
            return explanations[remedy_name]
            
        for key, value in explanations.items():
            if key in remedy_name:
                return value
                
        return "Natural aid for symptom relief."
