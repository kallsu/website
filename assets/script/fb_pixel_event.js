function LinkPageRedirect(element) {

    // Microservice 101 - Udemy
    if(element.id === "link_microservice_101_udemy"
        || element.id === "link2_microservice_101_udemy") 
    {
        fbq('track', 'ViewContent', 
			{
				content_name: "microservice_101_udemy", 
				content_type: "link", 
				contents: ["microservice_101", "udemy", "link"]
			});

        window.open('https://www.udemy.com/course/draft/3496088/?referralCode=B7658826178FCAB39521', '_blank');
    }
    // Azure Function - Udemy
    else if (element.id === "link_azurefunction_udemy"
                || element.id === "link2_azurefunction_udemy") 
    {
        fbq('track', 'ViewContent', 
			{
				content_name: "azure_function_udemy", 
				content_type: "link", 
				contents: ["azure_function", "udemy", "link"]
			});

        window.open('https://www.udemy.com/course/gd-azure-function/?referralCode=1D8BF46C6D3F8EFE05AB', '_blank');
    }

    return false;
}


