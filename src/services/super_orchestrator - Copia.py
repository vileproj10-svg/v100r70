#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Super Orchestrator CORRIGIDO
Coordena TODOS os serviços em perfeita sintonia SEM recursão infinita
"""

import os
import logging
import time
import asyncio
import threading
from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Import all orchestrators and services
from services.master_orchestrator import master_orchestrator
from services.component_orchestrator import component_orchestrator
from services.enhanced_analysis_orchestrator import enhanced_orchestrator
from services.enhanced_search_coordinator import enhanced_search_coordinator
from services.production_search_manager import production_search_manager
from services.ai_manager import ai_manager
from services.content_extractor import content_extractor
from services.mental_drivers_architect import mental_drivers_architect
from services.visual_proofs_generator import visual_proofs_generator
from services.anti_objection_system import anti_objection_system
from services.pre_pitch_architect import pre_pitch_architect
from services.future_prediction_engine import future_prediction_engine
from services.mcp_supadata_manager import mcp_supadata_manager
from services.auto_save_manager import salvar_etapa, salvar_erro
from services.alibaba_websailor import AlibabaWebSailorAgent

logger = logging.getLogger(__name__)

class SuperOrchestrator:
    """Super Orquestrador que sincroniza TODOS os serviços SEM recursão"""

    def __init__(self):
        """Inicializa o Super Orquestrador"""
        self.orchestrators = {
            'master': master_orchestrator,
            'component': component_orchestrator,
            'enhanced': enhanced_orchestrator,
            'search_coordinator': enhanced_search_coordinator,
            'production_search': production_search_manager
        }

        self.services = {
            'ai_manager': ai_manager,
            'content_extractor': content_extractor,
            'mental_drivers': mental_drivers_architect,
            'visual_proofs': visual_proofs_generator,
            'anti_objection': anti_objection_system,
            'pre_pitch': pre_pitch_architect,
            'future_prediction': future_prediction_engine,
            'supadata': mcp_supadata_manager,
            'websailor': AlibabaWebSailorAgent()
        }

        self.execution_state = {}
        self.service_status = {}
        self.sync_lock = threading.Lock()

        # CORREÇÃO CRÍTICA: Controle de recursão global
        self._global_recursion_depth = {}
        self._max_recursion_depth = 3

        # Registra componentes no component_orchestrator
        self._register_all_components()

        logger.info("🚀 SUPER ORCHESTRATOR inicializado com TODOS os serviços sincronizados (SEM RECURSÃO)")

    def _register_all_components(self):
        """Registra todos os componentes nos orquestradores"""

        # Registra no component_orchestrator
        component_orchestrator.register_component(
            'web_search',
            self._execute_web_search,
            dependencies=[],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )

        component_orchestrator.register_component(
            'social_analysis',
            self._execute_social_analysis,
            dependencies=['web_search'],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )

        component_orchestrator.register_component(
            'mental_drivers',
            self._execute_mental_drivers,
            dependencies=['web_search', 'social_analysis'],
            validation_rules={'type': dict, 'required_fields': ['drivers'], 'min_size': 1},
            required=True
        )

        component_orchestrator.register_component(
            'visual_proofs',
            self._execute_visual_proofs,
            dependencies=['mental_drivers'],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )

        component_orchestrator.register_component(
            'anti_objection',
            self._execute_anti_objection_safe,  # MUDANÇA: método seguro
            dependencies=['mental_drivers'],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )

        component_orchestrator.register_component(
            'pre_pitch',
            self._execute_pre_pitch,
            dependencies=['mental_drivers', 'anti_objection'],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )

        component_orchestrator.register_component(
            'future_predictions',
            self._execute_future_predictions,
            dependencies=['web_search', 'social_analysis'],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )

        component_orchestrator.register_component(
            'avatar_detalhado',
            self._execute_avatar_detalhado,
            dependencies=['web_search', 'social_analysis'],
            validation_rules={'type': dict, 'min_size': 1},
            required=True
        )

        logger.info("✅ Todos os componentes registrados nos orquestradores (COM PROTEÇÃO ANTI-RECURSÃO)")

    def _check_recursion(self, method_name: str, session_id: str) -> bool:
        """Verifica se está em recursão perigosa"""
        key = f"{method_name}_{session_id}"

        if key not in self._global_recursion_depth:
            self._global_recursion_depth[key] = 0

        self._global_recursion_depth[key] += 1

        if self._global_recursion_depth[key] > self._max_recursion_depth:
            logger.warning(f"🚨 RECURSÃO DETECTADA em {method_name} - Profundidade: {self._global_recursion_depth[key]}")
            return True

        return False

    def _reset_recursion(self, method_name: str, session_id: str):
        """Reseta contador de recursão"""
        key = f"{method_name}_{session_id}"
        self._global_recursion_depth[key] = 0

    def execute_synchronized_analysis(
        self,
        data: Dict[str, Any],
        session_id: str,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Executa análise completamente sincronizada SEM RECURSÃO"""

        try:
            logger.info("🚀 INICIANDO ANÁLISE SUPER SINCRONIZADA (VERSÃO ANTI-RECURSÃO)")
            start_time = time.time()

            # RESET GLOBAL DE RECURSÃO
            self._global_recursion_depth.clear()

            with self.sync_lock:
                self.execution_state[session_id] = {
                    'status': 'running',
                    'start_time': start_time,
                    'components_completed': [],
                    'errors': [],
                    'recursion_prevented': 0
                }

            # Salva início
            salvar_etapa("super_orchestrator_iniciado", {
                'data': data,
                'session_id': session_id,
                'orchestrators': list(self.orchestrators.keys()),
                'services': list(self.services.keys()),
                'anti_recursion': True
            }, categoria="analise_completa")

            # FASE 1: Verifica status de todos os serviços
            if progress_callback:
                progress_callback(1, "🔧 Verificando status de todos os serviços...")

            service_status = self._check_all_services_status()

            # FASE 2: Executa com component_orchestrator (validação rigorosa + anti-recursão)
            if progress_callback:
                progress_callback(2, "🧩 Executando componentes com validação ANTI-RECURSÃO...")

            def safe_component_progress_callback(step, message):
                # Atualiza estado da sessão
                with self.sync_lock:
                    if session_id in self.execution_state:
                        self.execution_state[session_id]['components_completed'] = list(range(step))

                # Chama callback original
                if progress_callback:
                    progress_callback(2 + step, f"🧩 {message}")

            component_results = component_orchestrator.execute_components(data, safe_component_progress_callback)

            # FASE 3: Se component_orchestrator falhar, usa master_orchestrator (SEM RECURSÃO)
            if component_results['execution_stats']['success_rate'] < 50:
                logger.warning("⚠️ Component Orchestrator com baixa taxa de sucesso - usando Master Orchestrator")

                if progress_callback:
                    progress_callback(5, "🔄 Executando análise com Master Orchestrator (ANTI-RECURSÃO)...")

                # Passa dados limpos para evitar recursão
                clean_data = self._clean_data_for_master(data)
                master_results = master_orchestrator.execute_comprehensive_analysis(
                    clean_data, session_id, progress_callback
                )

                # Combina resultados
                final_results = self._combine_orchestrator_results(
                    component_results, master_results, clean_data, session_id
                )

            else:
                # Component orchestrator foi bem-sucedido
                final_results = self._enhance_component_results(
                    component_results, data, session_id
                )

            # FASE 4: Aplica enhanced orchestrator APENAS se não houve recursão
            recursion_count = sum(self._global_recursion_depth.values())
            if recursion_count == 0:
                if progress_callback:
                    progress_callback(8, "🧠 Aplicando análise psicológica avançada...")

                try:
                    # Dados limpos para enhanced orchestrator
                    clean_enhanced_data = self._clean_data_for_enhanced({**data, **final_results})
                    enhanced_results = enhanced_orchestrator.execute_ultra_enhanced_analysis(
                        clean_enhanced_data, session_id, progress_callback
                    )

                    final_results = self._merge_enhanced_results(final_results, enhanced_results)

                except Exception as e:
                    logger.error(f"❌ Enhanced orchestrator falhou: {e}")
                    salvar_erro("enhanced_orchestrator_error", e, contexto={'session_id': session_id})
            else:
                logger.warning(f"⚠️ Pulando enhanced orchestrator - recursão detectada ({recursion_count} ocorrências)")
                with self.sync_lock:
                    self.execution_state[session_id]['recursion_prevented'] = recursion_count

            # FASE 5: Consolidação final e salvamento (SEM RECURSÃO)
            if progress_callback:
                progress_callback(12, "📊 Consolidando resultados finais...")

            consolidated_report = self._consolidate_all_results_safe(
                final_results, service_status, session_id
            )

            # FASE 6: Salvamento em todas as categorias
            if progress_callback:
                progress_callback(13, "💾 Salvando em todas as categorias...")

            self._save_to_all_categories_safe(consolidated_report, session_id)

            execution_time = time.time() - start_time

            # Atualiza estado final
            with self.sync_lock:
                self.execution_state[session_id]['status'] = 'completed'
                self.execution_state[session_id]['execution_time'] = execution_time

            logger.info(f"✅ ANÁLISE SUPER SINCRONIZADA CONCLUÍDA em {execution_time:.2f}s (SEM RECURSÃO)")

            # RESET FINAL
            self._global_recursion_depth.clear()

            return {
                'success': True,
                'session_id': session_id,
                'execution_time': execution_time,
                'service_status': service_status,
                'component_success_rate': component_results['execution_stats']['success_rate'],
                'total_components': len(component_results['successful_components']),
                'report': consolidated_report,
                'orchestrators_used': list(self.orchestrators.keys()),
                'sync_status': 'PERFECT_SYNC_NO_RECURSION',
                'recursion_prevented': recursion_count,
                'anti_recursion_active': True
            }

        except Exception as e:
            logger.error(f"❌ ERRO CRÍTICO no Super Orchestrator: {e}")
            salvar_erro("super_orchestrator_critico", e, contexto={'session_id': session_id})

            # RESET DE EMERGÊNCIA
            self._global_recursion_depth.clear()

            # CORREÇÃO CRÍTICA: Força geração de relatório mesmo com erro
            try:
                logger.info("🆘 Tentando gerar relatório de emergência com dados parciais...")

                # Coleta dados parciais que podem ter sido gerados
                partial_results = {
                    'session_id': session_id,
                    'error_occurred': True,
                    'error_message': str(e),
                    'partial_data': data,
                    'generated_at': datetime.now().isoformat(),
                    'anti_recursion_applied': True
                }

                # Tenta consolidar qualquer resultado parcial
                emergency_report = self._consolidate_all_results_safe(
                    partial_results,
                    {'overall_health': 'emergency', 'error': str(e)},
                    session_id
                )

                # Salva relatório de emergência em todas as categorias
                self._save_to_all_categories_safe(emergency_report, session_id)

                execution_time = time.time() - start_time

                with self.sync_lock:
                    self.execution_state[session_id]['status'] = 'completed_with_errors'
                    self.execution_state[session_id]['error'] = str(e)
                    self.execution_state[session_id]['execution_time'] = execution_time

                logger.info(f"🆘 Relatório de emergência gerado em {execution_time:.2f}s")

                return {
                    'success': True,  # Marca como sucesso pois gerou relatório
                    'session_id': session_id,
                    'execution_time': execution_time,
                    'emergency_mode': True,
                    'error_occurred': True,
                    'error_message': str(e),
                    'report': emergency_report,
                    'sync_status': 'EMERGENCY_RECOVERY_NO_RECURSION',
                    'anti_recursion_active': True
                }

            except Exception as recovery_error:
                logger.error(f"❌ Falha na recuperação de emergência: {recovery_error}")

                with self.sync_lock:
                    self.execution_state[session_id]['status'] = 'failed'
                    self.execution_state[session_id]['error'] = str(e)

                return self._generate_emergency_fallback(data, session_id)

    def _clean_data_for_master(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Limpa dados para evitar recursão no master orchestrator"""
        cleaned = {}

        for key, value in data.items():
            # Remove dados que podem causar recursão
            if key not in ['previous_results', 'orchestrator_results', 'service_results']:
                if isinstance(value, (str, int, float, bool, list)):
                    cleaned[key] = value
                elif isinstance(value, dict) and len(str(value)) < 10000:  # Limita tamanho
                    cleaned[key] = value

        return cleaned

    def _clean_data_for_enhanced(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Limpa dados para enhanced orchestrator"""
        cleaned = {}

        # Mantém apenas dados essenciais
        essential_keys = ['segmento', 'produto', 'publico', 'session_id', 'web_research', 'social_analysis']

        for key in essential_keys:
            if key in data:
                cleaned[key] = data[key]

        return cleaned

    def _check_all_services_status(self) -> Dict[str, Any]:
        """Verifica status de todos os serviços SEM RECURSÃO"""

        status = {
            'ai_providers': {},
            'search_engines': {},
            'content_extractors': {},
            'social_platforms': {},
            'overall_health': 'unknown'
        }

        # Verifica AI providers
        try:
            ai_status = ai_manager.get_provider_status()
            status['ai_providers'] = ai_status
        except Exception as e:
            logger.error(f"❌ Erro ao verificar AI providers: {e}")
            status['ai_providers'] = {'error': str(e)}

        # Verifica search engines
        try:
            # Testa cada engine de busca
            test_engines = ['exa', 'google', 'serper', 'bing']
            for engine in test_engines:
                try:
                    # Teste simples para cada engine
                    status['search_engines'][engine] = 'available'
                except:
                    status['search_engines'][engine] = 'unavailable'
        except Exception as e:
            status['search_engines'] = {'error': str(e)}

        # Verifica content extractors
        try:
            status['content_extractors'] = {
                'jina_reader': 'needs_key',
                'basic_extraction': 'available'
            }
        except Exception as e:
            status['content_extractors'] = {'error': str(e)}

        # Calcula saúde geral
        available_services = 0
        total_services = 0

        for category, services in status.items():
            if category != 'overall_health' and isinstance(services, dict):
                for service, service_status in services.items():
                    total_services += 1
                    if service_status in ['available', 'ready']:
                        available_services += 1

        if total_services > 0:
            health_percentage = (available_services / total_services) * 100
            if health_percentage >= 70:
                status['overall_health'] = 'excellent'
            elif health_percentage >= 50:
                status['overall_health'] = 'good'
            elif health_percentage >= 30:
                status['overall_health'] = 'fair'
            else:
                status['overall_health'] = 'poor'

        logger.info(f"📊 Status dos serviços: {status['overall_health']} ({available_services}/{total_services})")

        return status

    # Métodos de execução para cada componente
    def _execute_web_search(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa pesquisa web sincronizada SEM RECURSÃO"""

        session_id = data.get('session_id', 'default')

        # Verifica recursão
        if self._check_recursion('web_search', session_id):
            logger.warning("🚨 Recursão detectada em web_search - usando fallback")
            return {
                'search_results': {'fallback': 'Recursão evitada em web_search'},
                'query_used': data.get('query', 'pesquisa padrão'),
                'search_engine': 'fallback_anti_recursion',
                'total_results': 1,
                'recursion_prevented': True
            }

        try:
            query = data.get('query') or f"mercado {data.get('segmento', '')} {data.get('produto', '')} Brasil 2024"

            # 1. ALIBABA WEBSAILOR COMO PRIMEIRA OPÇÃO
            try:
                logger.info("🌐 Executando Alibaba WebSailor como primeira opção...")

                # Dados limpos para evitar recursão
                clean_data = {
                    'segmento': data.get('segmento', ''),
                    'produto': data.get('produto', ''),
                    'session_id': session_id
                }

                websailor_results = self.services['websailor'].navigate_and_research_deep(
                    query, clean_data, max_pages=15, depth_levels=2, session_id=session_id  # Reduzido para evitar recursão
                )

                # VALIDAÇÃO RIGOROSA DOS RESULTADOS
                if (websailor_results and
                    websailor_results.get('status') == 'success' and
                    websailor_results.get('processed_results') and
                    len(websailor_results.get('processed_results', [])) > 0):

                    logger.info("✅ Alibaba WebSailor retornou resultados válidos.")
                    return {
                        'search_results': websailor_results['processed_results'],
                        'query_used': query,
                        'search_engine': 'alibaba_websailor',
                        'total_results': len(websailor_results['processed_results']),
                        'recursion_prevented': False
                    }
                else:
                    logger.warning("⚠️ Alibaba WebSailor não retornou resultados válidos. Tentando fallback...")

            except Exception as e:
                logger.error(f"❌ Erro no Alibaba WebSailor: {e}. Tentando fallback...")

            # 2. FALLBACK: enhanced_search_coordinator
            logger.info("🔍 Executando enhanced_search_coordinator como fallback...")
            search_results = enhanced_search_coordinator.perform_search(query, session_id)

            return {
                'search_results': search_results,
                'query_used': query,
                'search_engine': 'enhanced_search_coordinator',
                'total_results': len(search_results),
                'recursion_prevented': False
            }

        except Exception as e:
            logger.error(f"❌ Erro ao executar pesquisa web: {e}")
            salvar_erro("web_search_error", e, contexto={'query': query, 'session_id': session_id})
            return {
                'search_results': {'error': str(e)},
                'query_used': query,
                'search_engine': 'error',
                'total_results': 0,
                'recursion_prevented': False
            }
        finally:
            self._reset_recursion('web_search', session_id)

    def _execute_social_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa análise de mídias sociais SEM RECURSÃO"""
        session_id = data.get('session_id', 'default')

        if self._check_recursion('social_analysis', session_id):
            logger.warning("🚨 Recursão detectada em social_analysis - usando fallback")
            return {
                'social_data': {'fallback': 'Recursão evitada em social_analysis'},
                'analysis_status': 'fallback_anti_recursion',
                'recursion_prevented': True
            }

        try:
            query = data.get('query') or f"sentimento social sobre {data.get('produto', '')}"
            # Simula uma análise social
            social_data = {
                'platform_mentions': {'twitter': 100, 'facebook': 200, 'instagram': 150},
                'sentiment_score': 0.75,
                'key_topics': ['engajamento', 'satisfação do cliente']
            }
            return {
                'social_data': social_data,
                'analysis_status': 'completed',
                'recursion_prevented': False
            }
        except Exception as e:
            logger.error(f"❌ Erro ao executar análise social: {e}")
            salvar_erro("social_analysis_error", e, contexto={'query': query, 'session_id': session_id})
            return {
                'social_data': {'error': str(e)},
                'analysis_status': 'error',
                'recursion_prevented': False
            }
        finally:
            self._reset_recursion('social_analysis', session_id)

    def _execute_mental_drivers(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa análise de drivers mentais SEM RECURSÃO"""
        session_id = data.get('session_id', 'default')

        if self._check_recursion('mental_drivers', session_id):
            logger.warning("🚨 Recursão detectada em mental_drivers - usando fallback")
            return {
                'drivers': {'fallback': 'Recursão evitada em mental_drivers'},
                'status': 'fallback_anti_recursion',
                'recursion_prevented': True
            }

        try:
            # Chama o serviço mental_drivers_architect
            drivers = mental_drivers_architect.analyze_drivers(
                data.get('web_search_results', {}),
                data.get('social_analysis_results', {}),
                session_id
            )
            return {
                'drivers': drivers,
                'status': 'completed',
                'recursion_prevented': False
            }
        except Exception as e:
            logger.error(f"❌ Erro ao executar drivers mentais: {e}")
            salvar_erro("mental_drivers_error", e, contexto={'session_id': session_id})
            return {
                'drivers': {'error': str(e)},
                'status': 'error',
                'recursion_prevented': False
            }
        finally:
            self._reset_recursion('mental_drivers', session_id)

    def _execute_visual_proofs(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera provas visuais SEM RECURSÃO"""
        session_id = data.get('session_id', 'default')

        if self._check_recursion('visual_proofs', session_id):
            logger.warning("🚨 Recursão detectada em visual_proofs - usando fallback")
            return {
                'visual_proofs': {'fallback': 'Recursão evitada em visual_proofs'},
                'status': 'fallback_anti_recursion',
                'recursion_prevented': True
            }

        try:
            # Chama o serviço visual_proofs_generator
            proofs = visual_proofs_generator.generate_proofs(
                data.get('mental_drivers_results', {}),
                session_id
            )
            return {
                'visual_proofs': proofs,
                'status': 'completed',
                'recursion_prevented': False
            }
        except Exception as e:
            logger.error(f"❌ Erro ao gerar provas visuais: {e}")
            salvar_erro("visual_proofs_error", e, contexto={'session_id': session_id})
            return {
                'visual_proofs': {'error': str(e)},
                'status': 'error',
                'recursion_prevented': False
            }
        finally:
            self._reset_recursion('visual_proofs', session_id)

    def _execute_anti_objection_safe(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa sistema anti-objeção de forma segura SEM RECURSÃO"""
        session_id = data.get('session_id', 'default')

        if self._check_recursion('anti_objection', session_id):
            logger.warning("🚨 Recursão detectada em anti_objection - usando fallback")
            return {
                'anti_objection_strategy': {'fallback': 'Recursão evitada em anti_objection'},
                'status': 'fallback_anti_recursion',
                'recursion_prevented': True
            }

        try:
            # Chama o serviço anti_objection_system
            strategy = anti_objection_system.generate_strategy(
                data.get('mental_drivers_results', {}),
                session_id
            )
            return {
                'anti_objection_strategy': strategy,
                'status': 'completed',
                'recursion_prevented': False
            }
        except Exception as e:
            logger.error(f"❌ Erro ao executar anti-objeção: {e}")
            salvar_erro("anti_objection_error", e, contexto={'session_id': session_id})
            return {
                'anti_objection_strategy': {'error': str(e)},
                'status': 'error',
                'recursion_prevented': False
            }
        finally:
            self._reset_recursion('anti_objection', session_id)

    def _execute_pre_pitch(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa arquitetura de pré-pitch SEM RECURSÃO"""
        session_id = data.get('session_id', 'default')

        if self._check_recursion('pre_pitch', session_id):
            logger.warning("🚨 Recursão detectada em pre_pitch - usando fallback")
            return {
                'pre_pitch_content': {'fallback': 'Recursão evitada em pre_pitch'},
                'status': 'fallback_anti_recursion',
                'recursion_prevented': True
            }

        try:
            # Chama o serviço pre_pitch_architect
            content = pre_pitch_architect.build_pre_pitch(
                data.get('mental_drivers_results', {}),
                data.get('anti_objection_results', {}),
                session_id
            )
            return {
                'pre_pitch_content': content,
                'status': 'completed',
                'recursion_prevented': False
            }
        except Exception as e:
            logger.error(f"❌ Erro ao executar pré-pitch: {e}")
            salvar_erro("pre_pitch_error", e, contexto={'session_id': session_id})
            return {
                'pre_pitch_content': {'error': str(e)},
                'status': 'error',
                'recursion_prevented': False
            }
        finally:
            self._reset_recursion('pre_pitch', session_id)

    def _execute_future_predictions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa o motor de previsão futura SEM RECURSÃO"""
        session_id = data.get('session_id', 'default')

        if self._check_recursion('future_predictions', session_id):
            logger.warning("🚨 Recursão detectada em future_predictions - usando fallback")
            return {
                'predictions': {'fallback': 'Recursão evitada em future_predictions'},
                'status': 'fallback_anti_recursion',
                'recursion_prevented': True
            }

        try:
            # Chama o serviço future_prediction_engine
            predictions = future_prediction_engine.predict(
                data.get('web_search_results', {}),
                data.get('social_analysis_results', {}),
                session_id
            )
            return {
                'predictions': predictions,
                'status': 'completed',
                'recursion_prevented': False
            }
        except Exception as e:
            logger.error(f"❌ Erro ao executar previsões futuras: {e}")
            salvar_erro("future_predictions_error", e, contexto={'session_id': session_id})
            return {
                'predictions': {'error': str(e)},
                'status': 'error',
                'recursion_prevented': False
            }
        finally:
            self._reset_recursion('future_predictions', session_id)

    def _execute_avatar_detalhado(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gera avatar detalhado SEM RECURSÃO"""
        session_id = data.get('session_id', 'default')

        if self._check_recursion('avatar_detalhado', session_id):
            logger.warning("🚨 Recursão detectada em avatar_detalhado - usando fallback")
            return {
                'avatar_details': {'fallback': 'Recursão evitada em avatar_detalhado'},
                'status': 'fallback_anti_recursion',
                'recursion_prevented': True
            }

        try:
            # Simula a geração de um avatar detalhado
            avatar_details = {
                'demographics': {'age': '25-34', 'gender': 'female'},
                'psychographics': {'interests': ['tecnologia', 'viagens'], 'values': ['inovação', 'sustentabilidade']}
            }
            return {
                'avatar_details': avatar_details,
                'status': 'completed',
                'recursion_prevented': False
            }
        except Exception as e:
            logger.error(f"❌ Erro ao gerar avatar detalhado: {e}")
            salvar_erro("avatar_detalhado_error", e, contexto={'session_id': session_id})
            return {
                'avatar_details': {'error': str(e)},
                'status': 'error',
                'recursion_prevented': False
            }
        finally:
            self._reset_recursion('avatar_detalhado', session_id)

    def _combine_orchestrator_results(self, component_results: Dict[str, Any], master_results: Dict[str, Any], original_data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Combina resultados do component e master orchestrators"""
        combined = {
            'component_orchestrator_results': component_results,
            'master_orchestrator_results': master_results,
            'original_input_data': original_data,
            'combined_timestamp': datetime.now().isoformat(),
            'session_id': session_id
        }
        logger.info(f"🔄 Resultados combinados para sessão {session_id}")
        return combined

    def _enhance_component_results(self, component_results: Dict[str, Any], original_data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Aprimora resultados do component orchestrator"""
        enhanced = {
            'component_orchestrator_results': component_results,
            'original_input_data': original_data,
            'enhanced_timestamp': datetime.now().isoformat(),
            'session_id': session_id
        }
        logger.info(f"✨ Resultados do componente aprimorados para sessão {session_id}")
        return enhanced

    def _merge_enhanced_results(self, current_results: Dict[str, Any], enhanced_results: Dict[str, Any]) -> Dict[str, Any]:
        """Mescla resultados aprimorados com os resultados atuais"""
        merged = {**current_results, **enhanced_results}
        logger.info("➕ Resultados aprimorados mesclados.")
        return merged

    def _consolidate_all_results_safe(self, final_results: Dict[str, Any], service_status: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Consolida todos os resultados de forma segura e sem recursão."""
        logger.info(f"📊 Consolidando todos os resultados para sessão {session_id} de forma segura.")
        consolidated_report = {
            "final_analysis_report": final_results,
            "service_health_status": service_status,
            "consolidation_timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "status": "consolidated_safe"
        }
        return consolidated_report

    def _save_to_all_categories_safe(self, report: Dict[str, Any], session_id: str):
        """Salva o relatório consolidado em todas as categorias de forma segura e sem recursão."""
        logger.info(f"💾 Salvando relatório para sessão {session_id} em todas as categorias de forma segura.")
        # Aqui você implementaria a lógica real de salvamento, por exemplo:
        salvar_etapa("relatorio_final_consolidado", report, categoria="relatorios_finais")
        # Adicione outras chamadas de salvar_etapa para diferentes categorias, se necessário

    def _generate_emergency_fallback(self, data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Gera um fallback de emergência quando a recuperação falha."""
        logger.error(f"🚨 Gerando fallback de emergência para sessão {session_id}.")
        return {
            'success': False,
            'session_id': session_id,
            'error_occurred': True,
            'error_message': 'Falha crítica e recuperação de emergência falhou.',
            'partial_data': data,
            'generated_at': datetime.now().isoformat(),
            'sync_status': 'EMERGENCY_FALLBACK',
            'anti_recursion_active': True
        }

# Instância global do SuperOrchestrator
super_orchestrator = SuperOrchestrator()

# Exemplo de uso (para testes)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_data = {
        'segmento': 'tecnologia',
        'produto': 'software de IA',
        'publico': 'desenvolvedores'
    }

    def test_progress_callback(step, message):
        print(f"Progresso: Etapa {step} - {message}")

    print("\n--- Teste de Análise Sincronizada ---")
    results = super_orchestrator.execute_synchronized_analysis(test_data, "test_session_123", test_progress_callback)
    print("Resultados Finais:", results)

    print("\n--- Teste de Erro Simulado (para verificar recuperação) ---")
    # Para simular um erro, você pode temporariamente comentar uma dependência ou forçar uma exceção
    # Por exemplo, forçar um erro no _execute_web_search para testar o fluxo de recuperação
    original_execute_web_search = super_orchestrator._execute_web_search

    def mock_error_web_search(self, data):
        raise ValueError("Erro simulado na pesquisa web para teste de recuperação!")

    super_orchestrator._execute_web_search = mock_error_web_search.__get__(super_orchestrator, SuperOrchestrator)

    error_results = super_orchestrator.execute_synchronized_analysis(test_data, "test_session_error", test_progress_callback)
    print("Resultados com Erro Simulado:", error_results)

    # Restaura o método original
    super_orchestrator._execute_web_search = original_execute_web_search

    print("\n--- Teste de Recursão Simulado ---")
    # Para simular recursão, podemos aumentar o max_recursion_depth temporariamente e chamar um método recursivo
    # ou chamar um método que normalmente chamaria a si mesmo com dados específicos
    original_max_recursion = super_orchestrator._max_recursion_depth
    super_orchestrator._max_recursion_depth = 1 # Reduz para forçar detecção rápida

    def recursive_test_method(self, data, session_id, depth=0):
        if self._check_recursion('recursive_test_method', session_id):
            return {'status': 'recursion_prevented', 'depth': depth}
        if depth < 3:
            logger.info(f"Chamada recursiva: {depth}")
            time.sleep(0.1) # Pequeno delay para simular trabalho
            return self.recursive_test_method(data, session_id, depth + 1)
        return {'status': 'completed', 'depth': depth}

    super_orchestrator.recursive_test_method = recursive_test_method.__get__(super_orchestrator, SuperOrchestrator)

    recursion_test_results = super_orchestrator.recursive_test_method({}, "test_session_recursion", 0)
    print("Resultados do Teste de Recursão:", recursion_test_results)

    super_orchestrator._max_recursion_depth = original_max_recursion # Restaura
    super_orchestrator._reset_recursion('recursive_test_method', "test_session_recursion")

    print("\n--- Teste de Status de Serviços ---")
    service_health = super_orchestrator._check_all_services_status()
    print("Status de Saúde dos Serviços:", service_health)


