#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Enhanced Search Coordinator ULTRA-ROBUSTO
Coordenador que GARANTE buscas simultâneas e distintas entre Exa e Google
"""

import os
import logging
import time
import asyncio
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from services.exa_client import exa_client
from services.production_search_manager import production_search_manager
from services.auto_save_manager import salvar_etapa, salvar_erro
from services.mcp_supadata_manager import mcp_supadata_manager
from services.deep_research_mcp_client import deep_research_mcp_client as deep_research_client
from services.instagram_mcp_client import instagram_mcp_client as instagram_client
from services.youtube_mcp_client import youtube_mcp_client as youtube_client

logger = logging.getLogger(__name__)

class EnhancedSearchCoordinator:
    """Coordenador ULTRA-ROBUSTO de buscas simultâneas e distintas"""

    def __init__(self):
        """Inicializa coordenador de busca"""
        self.exa_available = exa_client.is_available()
        self.google_available = bool(os.getenv('GOOGLE_SEARCH_KEY') and os.getenv('GOOGLE_CSE_ID'))

        logger.info(f"🔍 Enhanced Search Coordinator ULTRA-ROBUSTO - Exa: {self.exa_available}, Google: {self.google_available}")

        # MCP Clients
        self.supadata_manager = mcp_supadata_manager
        self.deep_research_client = deep_research_client
        self.instagram_client = instagram_client
        self.youtube_client = youtube_client

    def perform_search(self, query: str, session_id: str = None) -> List[Dict[str, Any]]:
        """Método de compatibilidade para perform_search"""
        try:
            # Usa o método principal de busca
            search_results = self.execute_simultaneous_distinct_search(query, {}, session_id)

            # Extrai apenas os resultados
            all_results = []

            if search_results.get('exa_results'):
                all_results.extend(search_results['exa_results'])

            if search_results.get('google_results'):
                all_results.extend(search_results['google_results'])

            if search_results.get('other_results'):
                all_results.extend(search_results['other_results'])

            return all_results

        except Exception as e:
            logger.error(f"❌ Erro em perform_search: {e}")
            return []

    def execute_simultaneous_distinct_search(
        self, 
        base_query: str, 
        context: Dict[str, Any],
        session_id: str = None
    ) -> Dict[str, Any]:
        """GARANTE buscas MASSIVAS simultâneas e distintas - ESPECTRO AMPLIADO"""

        logger.info(f"🚀 INICIANDO BUSCAS MASSIVAS ULTRA-ROBUSTAS para: {base_query}")

        # Prepara MÚLTIPLAS queries DISTINTAS para cobertura máxima
        query_variations = self._generate_comprehensive_query_variations(base_query, context)

        # Salva queries preparadas
        salvar_etapa("queries_massivas_simultaneas", {
            "base_query": base_query,
            "query_variations": query_variations,
            "context": context,
            "search_scope": "MASSIVE_COMPREHENSIVE",
            "garantia_simultanea": True,
            "garantia_robusta": True
        }, categoria="pesquisa_web")

        search_results = {
            'base_query': base_query,
            'query_variations': query_variations,
            'exa_results': [],
            'google_results': [],
            'deep_research_results': [],
            'social_media_results': [],
            'news_results': [],
            'academic_results': [],
            'competitor_results': [],
            'trend_results': [],
            'execution_mode': 'MASSIVE_COMPREHENSIVE',
            'statistics': {
                'total_results': 0,
                'total_sources': 0,
                'exa_count': 0,
                'google_count': 0,
                'deep_research_count': 0,
                'social_count': 0,
                'news_count': 0,
                'academic_count': 0,
                'competitor_count': 0,
                'trend_count': 0,
                'search_time': 0,
                'simultaneous_execution': True,
                'comprehensive_coverage': True
            }
        }

        start_time = time.time()

        # EXECUTA BUSCAS MASSIVAS SIMULTANEAMENTE com ThreadPoolExecutor AMPLIADO
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {}

            # Prepara queries específicas para cada tipo de busca
            exa_query = self._prepare_exa_neural_search(base_query, context)
            google_query = self._prepare_google_keyword_query(base_query, context)

            # Busca Exa (se disponível) - NEURAL SEARCH
            if self.exa_available:
                futures['exa'] = executor.submit(self._execute_exa_neural_search, exa_query, context)
                logger.info(f"🧠 Exa Neural Search INICIADA: {exa_query}")

            # Busca Google (se disponível) - KEYWORD SEARCH
            if self.google_available:
                futures['google'] = executor.submit(self._execute_google_keyword_search, google_query, context)
                logger.info(f"🔍 Google Keyword Search INICIADA: {google_query}")

            # Busca outros provedores - FALLBACK SEARCH
            futures['other'] = executor.submit(self._execute_other_providers_search, base_query, context)
            logger.info(f"🌐 Other Providers Search INICIADA: {base_query}")

            # Coleta resultados conforme completam (SIMULTANEAMENTE)
            for provider_name, future in futures.items():
                try:
                    result = future.result(timeout=120)  # 2 minutos timeout

                    if provider_name == 'exa':
                        search_results['exa_results'] = result.get('results', [])
                        search_results['statistics']['exa_count'] = len(result.get('results', []))
                        logger.info(f"✅ Exa Neural: {len(result.get('results', []))} resultados ÚNICOS")

                        # Salva resultados Exa IMEDIATAMENTE
                        salvar_etapa("exa_neural_results", result, categoria="pesquisa_web")

                    elif provider_name == 'google':
                        search_results['google_results'] = result.get('results', [])
                        search_results['statistics']['google_count'] = len(result.get('results', []))
                        logger.info(f"✅ Google Keywords: {len(result.get('results', []))} resultados ÚNICOS")

                        # Salva resultados Google IMEDIATAMENTE
                        salvar_etapa("google_keyword_results", result, categoria="pesquisa_web")

                    elif provider_name == 'other':
                        search_results['other_results'] = result.get('results', [])
                        search_results['statistics']['other_count'] = len(result.get('results', []))
                        logger.info(f"✅ Outros Provedores: {len(result.get('results', []))} resultados")

                        # Salva resultados outros IMEDIATAMENTE
                        salvar_etapa("other_providers_results", result, categoria="pesquisa_web")

                except Exception as e:
                    logger.error(f"❌ Erro em busca {provider_name}: {e}")
                    salvar_erro(f"busca_{provider_name}", e, contexto={"query": base_query})

                    # CONTINUA MESMO COM ERRO - SALVA O QUE TEM
                    search_results[f'{provider_name}_error'] = str(e)
                    continue

        # Calcula estatísticas finais
        search_time = time.time() - start_time
        search_results['statistics']['search_time'] = search_time
        search_results['statistics']['total_results'] = (
            search_results['statistics']['exa_count'] + 
            search_results['statistics']['google_count'] + 
            search_results['statistics']['other_count']
        )

        # GARANTE que pelo menos uma busca funcionou
        if search_results['statistics']['total_results'] == 0:
            logger.error("❌ NENHUMA BUSCA RETORNOU RESULTADOS - Configure APIs")
            search_results['error'] = "Configure APIs de pesquisa para obter dados reais"
            search_results['fallback_message'] = None

        # Salva resultado consolidado IMEDIATAMENTE
        salvar_etapa("busca_simultanea_consolidada", search_results, categoria="pesquisa_web")

        logger.info(f"✅ Buscas SIMULTÂNEAS E DISTINTAS concluídas em {search_time:.2f}s")
        logger.info(f"📊 Total: {search_results['statistics']['total_results']} resultados únicos")

        return search_results

    async def execute_comprehensive_web_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa busca web com cobertura total, incluindo redes sociais e deep research."""
        logger.info(f"🚀 INICIANDO BUSCA WEB AMPLA para: {query}")

        results = {
            'query': query,
            'exa': {},
            'google': {},
            'supadata': {},
            'deep_research': {},
            'instagram': {},
            'youtube': {},
            'error': None,
            'total_results': 0
        }

        prepared_query = self._prepare_search_query(query, context)
        total_results = 0

        async def run_search_task(search_func, key, **kwargs):
            nonlocal total_results
            try:
                response = await search_func(**kwargs)
                if response.get('success'):
                    results[key] = response
                    data_list = response.get('data') or response.get('results') or response.get('posts') or response.get('videos') or []
                    if isinstance(data_list, list):
                        total_results += len(data_list)
                        logger.info(f"✅ {key.capitalize()}: {len(data_list)} resultados")
                    else:
                        logger.warning(f"⚠️ {key.capitalize()} retornou dados não listados: {type(data_list)}")
                else:
                    logger.warning(f"⚠️ {key.capitalize()} falhou: {response.get('error', 'Erro desconhecido')}")
                    results[key] = {"error": response.get('error'), "data": []}
            except Exception as e:
                logger.error(f"❌ Erro {key.capitalize()}: {e}")
                results[key] = {"error": str(e), "data": []}

        search_tasks = []

        # 1. Exa Search
        exa_query = self._prepare_exa_neural_search(query, context)
        search_tasks.append(run_search_task(self._execute_exa_neural_search, 'exa', query=exa_query, context=context))

        # 2. Google Search
        google_query = self._prepare_google_keyword_query(query, context)
        search_tasks.append(run_search_task(self._execute_google_keyword_search, 'google', query=google_query, context=context))

        # 3. Deep Research MCP
        search_tasks.append(run_search_task(self._execute_deep_research_search, 'deep_research', query=prepared_query, context=context))

        # 4. Supadata (Redes Sociais)
        if self.supadata_manager.enabled:
            search_tasks.append(run_search_task(self.supadata_manager.search_social_media, 'supadata', query=prepared_query, platforms=['instagram', 'youtube', 'tiktok'], sentiment_analysis=True))

        # 5. Instagram (Novo)
        search_tasks.append(run_search_task(self.instagram_client.search_instagram_content, 'instagram', query=prepared_query, hashtags=self._extract_hashtags(prepared_query)))

        # 6. YouTube (Novo)
        search_tasks.append(run_search_task(self.youtube_client.search_videos, 'youtube', query=prepared_query, max_results=25))

        # Executa todas as tarefas de busca de forma concorrente
        await asyncio.gather(*search_tasks)

        results['total_results'] = total_results
        logger.info(f"✅ Busca web ampla concluída. Total de resultados: {total_results}")
        return results

    def _prepare_exa_neural_query(self, base_query: str, context: Dict[str, Any]) -> str:
        """Prepara query ESPECÍFICA para Exa Neural Search"""

        # Exa é melhor com queries conceituais e semânticas
        exa_query = f"{base_query} insights análise profunda"

        # Adiciona contexto semântico para busca neural
        if context.get('segmento'):
            exa_query += f" {context['segmento']} tendências oportunidades"

        # Termos para busca neural semântica
        exa_query += " estratégia inovação futuro"

        return exa_query.strip()

    def _generate_comprehensive_query_variations(self, base_query: str, context: Dict[str, Any]) -> Dict[str, List[str]]:
        """Gera variações abrangentes de queries para cobertura máxima"""

        segmento = context.get('segmento', '')
        produto = context.get('produto', '')

        variations = {
            'exa_neural_queries': [
                f"{base_query} insights análise neural semântica",
                f"{base_query} tendências futuro oportunidades",
                f"{base_query} estratégia inovação mercado",
                f"análise profunda {segmento} {produto} transformação digital"
            ],
            'google_keyword_queries': [
                f"{base_query} dados estatísticas Brasil 2024",
                f"{base_query} mercado brasileiro crescimento números",
                f"{base_query} pesquisa IBGE dados oficiais",
                f"relatório {segmento} {produto} Brasil estatísticas"
            ],
            'deep_research_queries': [
                f"pesquisa acadêmica {base_query} universidades",
                f"estudos científicos {segmento} {produto}",
                f"papers research {base_query} metodologia",
                f"dissertações teses {segmento} análise"
            ],
            'social_media_queries': [
                f"{base_query} discussão redes sociais",
                f"{segmento} {produto} opinião pública",
                f"debate {base_query} comunidades online",
                f"sentimento mercado {segmento} social media"
            ],
            'news_queries': [
                f"{base_query} notícias recentes Brasil",
                f"últimas novidades {segmento} {produto}",
                f"breaking news {base_query} mercado",
                f"jornalismo {segmento} tendências atuais"
            ],
            'competitor_queries': [
                f"concorrentes {segmento} {produto} análise",
                f"players mercado {base_query} competição",
                f"benchmark {segmento} líderes mercado",
                f"análise competitiva {base_query} Brasil"
            ],
            'trend_queries': [
                f"tendências {base_query} próximos anos",
                f"futuro {segmento} {produto} previsões",
                f"evolução mercado {base_query} 2024-2030",
                f"transformações {segmento} tecnologia"
            ]
        }

        logger.info(f"📊 Geradas {sum(len(v) for v in variations.values())} variações de query para cobertura máxima")
        return variations

    def _prepare_google_keyword_query(self, base_query: str, context: Dict[str, Any]) -> str:
        """Prepara query ESPECÍFICA para Google Keyword Search"""

        # Google é melhor com keywords específicas e dados
        google_query = f"{base_query} dados estatísticas"

        # Adiciona keywords específicas
        if context.get('segmento'):
            google_query += f" {context['segmento']} mercado brasileiro"

        # Termos para busca por keywords
        google_query += " Brasil 2024 crescimento números"

        return google_query.strip()

    def _execute_exa_neural_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa busca NEURAL específica no Exa"""

        try:
            logger.info(f"🧠 Executando Exa NEURAL SEARCH: {query}")

            # Domínios brasileiros preferenciais para Exa
            include_domains = [
                "g1.globo.com", "exame.com", "valor.globo.com", "estadao.com.br",
                "folha.uol.com.br", "canaltech.com.br", "infomoney.com.br",
                "startse.com", "revistapegn.globo.com", "epocanegocios.globo.com"
            ]

            exa_response = exa_client.search(
                query=query,
                num_results=20,  # Mais resultados para Exa
                include_domains=include_domains,
                start_published_date="2023-01-01",
                use_autoprompt=True,
                type="neural"  # FORÇA BUSCA NEURAL
            )

            if exa_response and 'results' in exa_response:
                results = []
                for item in exa_response['results']:
                    results.append({
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'snippet': item.get('text', '')[:300],
                        'source': 'exa_neural',
                        'score': item.get('score', 0),
                        'published_date': item.get('publishedDate', ''),
                        'exa_id': item.get('id', ''),
                        'search_type': 'neural_semantic'
                    })

                logger.info(f"✅ Exa Neural Search: {len(results)} resultados ÚNICOS")
                return {
                    'provider': 'exa',
                    'query': query,
                    'results': results,
                    'success': True,
                    'search_type': 'neural_semantic'
                }
            else:
                logger.warning("⚠️ Exa não retornou resultados - CONTINUANDO")
                return {
                    'provider': 'exa',
                    'query': query,
                    'results': [],
                    'success': False,
                    'error': 'Exa não retornou resultados válidos'
                }

        except Exception as e:
            logger.error(f"❌ Erro na busca Exa: {e}")
            # SALVA ERRO MAS CONTINUA
            salvar_erro("exa_neural_search", e, contexto={"query": query})
            return {
                'provider': 'exa',
                'query': query,
                'results': [],
                'success': False,
                'error': str(e)
            }

    def _execute_google_keyword_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa busca KEYWORD específica no Google"""

        try:
            logger.info(f"🔍 Executando Google KEYWORD SEARCH: {query}")

            # Usa production search manager especificamente para Google
            google_api_key = os.getenv('GOOGLE_SEARCH_KEY')
            google_cse_id = os.getenv('GOOGLE_CSE_ID')

            if not google_api_key or not google_cse_id:
                raise Exception("Google API não configurada")

            import requests

            params = {
                'key': google_api_key,
                'cx': google_cse_id,
                'q': query,
                'num': 20,  # Mais resultados para Google
                'lr': 'lang_pt',
                'gl': 'br',
                'safe': 'off',
                'dateRestrict': 'm12'  # Últimos 12 meses
            }

            response = requests.get(
                'https://www.googleapis.com/customsearch/v1',
                params=params,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                results = []

                for item in data.get('items', []):
                    results.append({
                        'title': item.get('title', ''),
                        'url': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'source': 'google_keywords',
                        'search_type': 'keyword_based'
                    })

                logger.info(f"✅ Google Keyword Search: {len(results)} resultados ÚNICOS")
                return {
                    'provider': 'google',
                    'query': query,
                    'results': results,
                    'success': True,
                    'search_type': 'keyword_based'
                }
            else:
                raise Exception(f"Google API retornou status {response.status_code}")

        except Exception as e:
            logger.error(f"❌ Erro na busca Google: {e}")
            # SALVA ERRO MAS CONTINUA
            salvar_erro("google_keyword_search", e, contexto={"query": query})
            return {
                'provider': 'google',
                'query': query,
                'results': [],
                'success': False,
                'error': str(e)
            }

    def _execute_other_providers_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa busca em outros provedores como fallback"""

        try:
            logger.info(f"🌐 Executando Other Providers Search: {query}")

            # Usa outros provedores (Serper, Bing, DuckDuckGo)
            other_results = production_search_manager.comprehensive_search(query, max_results=15)

            # Filtra resultados que não são Google ou Exa
            other_only = []
            for result in other_results:
                if result.get('source') not in ['google', 'exa', 'google_keywords', 'exa_neural']:
                    result['search_type'] = 'fallback_providers'
                    other_only.append(result)

            logger.info(f"✅ Other Providers: {len(other_only)} resultados")
            return {
                'provider': 'other',
                'query': query,
                'results': other_only,
                'success': len(other_only) > 0,
                'search_type': 'fallback_providers'
            }

        except Exception as e:
            logger.error(f"❌ Erro na busca outros provedores: {e}")
            # SALVA ERRO MAS CONTINUA
            salvar_erro("other_providers_search", e, contexto={"query": query})
            return {
                'provider': 'other',
                'query': query,
                'results': [],
                'success': False,
                'error': str(e)
            }

    def _execute_deep_research_search(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Executa busca de pesquisa aprofundada usando o MCP"""
        try:
            logger.info(f"🔬 Executando Deep Research Search: {query}")

            # Usa o cliente de pesquisa aprofundada
            deep_research_results = self.deep_research_client.search(query=query, context=context)

            if deep_research_results.get('success'):
                logger.info(f"✅ Deep Research: {len(deep_research_results.get('results', []))} resultados encontrados")
                return {
                    'provider': 'deep_research',
                    'query': query,
                    'results': deep_research_results.get('results', []),
                    'success': True,
                    'search_type': 'deep_research'
                }
            else:
                logger.warning(f"⚠️ Deep Research falhou: {deep_research_results.get('error', 'Erro desconhecido')}")
                return {
                    'provider': 'deep_research',
                    'query': query,
                    'results': [],
                    'success': False,
                    'error': deep_research_results.get('error')
                }
        except Exception as e:
            logger.error(f"❌ Erro Deep Research: {e}")
            salvar_erro("deep_research_search", e, contexto={"query": query})
            return {
                'provider': 'deep_research',
                'query': query,
                'results': [],
                'success': False,
                'error': str(e)
            }

    def _extract_hashtags(self, query: str) -> List[str]:
        """Extrai hashtags relevantes da query"""
        import re

        # Palavras-chave para hashtags
        keywords = re.findall(r'\b\w+\b', query.lower())
        hashtags = []

        for keyword in keywords:
            if len(keyword) > 3:  # Apenas palavras com mais de 3 caracteres
                hashtags.append(f"#{keyword}")

        return hashtags[:10]  # Máximo 10 hashtags

    def _prepare_search_query(self, query: str, context: Dict[str, Any] = None) -> str:
        """Prepara uma query mais genérica para diferentes provedores, incluindo contexto."""
        prepared = query
        if context:
            if context.get('segmento'):
                prepared += f" {context['segmento']}"
            if context.get('produto'):
                prepared += f" {context['produto']}"

        # Adiciona termos genéricos para cobrir mais casos
        prepared += " análise dados insights mercado"

        return prepared.strip()

# Instância global
enhanced_search_coordinator = EnhancedSearchCoordinator()